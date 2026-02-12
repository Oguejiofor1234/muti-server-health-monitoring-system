'''Remote Multi-Server Health Monitoring System
Monitors multiple servers via SSH and sends alerts when thresholds are breached'''
import paramiko
import time
import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import SERVERS, THRESHOLDS, EMAIL_CONFIG, MONITORING_CONFIG, LOG_FILE, ALERT_LOG_FILE

class ServerMonitor:
    '''Monitor a single server via SSH'''

    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.client = None
        self.last_alert_time = {}  # Track when we last alerted for each metric
    
    def connect(self):
        '''Establish SSH connection to server'''
        try: 
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            self.client.connect(
                hostname = self.config['hostname'],
                port=self.config['port'],
                username=self.config['username'],
                key_filename=self.config['key_filename'],
                timeout=10
            )
            return True
        except Exception as e:
            print(f"x Failed to connect to {self.name}: {e}")
            return False
    def disconnect(self):
        '''Close SSH connection'''
        if self.client:
            self.client.close()
    
    def execute_command(self, command):
        '''Execute command on remote server and return output'''
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_code = stdout.channel.recv_exit_status()

            if exit_code == 0:
                return stdout.read().decode('utf-8').strip()
            else:
                error =stderr.read().decode('utf-8').strip()
                print(f"Command filed on {self.name}: {error}")
                return None
        
        except Exception as e:
            print(f"x Error executing command on {self.name}: {e}")
    
    def get_metrics(self):
        '''Collect all health metrics from server'''
        metrics = {
            'server_name': self.name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'unknown',
            'cpu_percent': None,
            'memory_percent': None,
            'disk_percent': None,
            'uptime': None
        }

        # Connect to server
        if not self.connect():
            metrics['status'] = 'unreachable'
            return metrics 
        
        try:
            # CPU Usage
            cpu_cmd = "python3 -c \"import psutil; print(psutil.cpu_percent(interval=1))\""
            cpu_result = self.execute_command(cpu_cmd)
            if cpu_result:
                metrics['cpu_percent'] = float(cpu_result)
            
             # Memory Usage
            mem_cmd = "python3 -c \"import psutil; print(psutil.virtual_memory().percent)\""
            mem_result = self.execute_command(mem_cmd)
            if mem_result:
                metrics['memory_percent'] = float(mem_result)

             # Disk Usage
            disk_cmd = "python3 -c \"import psutil; print(psutil.disk_usage('/').percent)\""
            disk_result = self.execute_command(disk_cmd)   
            if disk_result:
                metrics['disk_percent'] = float(disk_result)

            # Uptime
            uptime_cmd = "uptime -p"
            uptime_result = self.execute_command(uptime_cmd)
            if uptime_result:
                metrics['uptime'] = uptime_result

            metrics['status'] = 'healthy' 

        except Exception as e:
            print(f"x Error collecting metrics from {self.name}: {e}")
            metrics['status'] = 'error' 
        
        finally:
            self.disconnect()
        return metrics
    
    def check_thresholds(self, metrics):
        """Check if any metrics exceed thresholds"""
        alerts =[]

        # Check CPU 
        if metrics['cpu_percent'] is not None and metrics['cpu_percent'] > THRESHOLDS['cpu_percent']:
            if self._should_alert('cpu'):
                alerts.append({
                    'type': 'CPU',
                    'current': metrics['cpu_percent'],
                    'thresholds': THRESHOLDS['cpu_percent']

                })
                self.last_alert_time['cpu'] = time.time()
        
        # Check Memory
        if metrics['memory_percent'] is not None and metrics['memory_percent'] > THRESHOLDS['memory_percent']:
            if self._should_alert('memory'):
                alerts.append({
                    'type': 'Memory',
                    'current': metrics['memory_percent'],
                    'thresholds': THRESHOLDS['memory_percent']

                })
                self.last_alert_time['memory'] = time.time()

        # Check Disk
        if metrics['disk_percent'] is not None and metrics['disk_percent'] > THRESHOLDS['disk_percent']:
            if self._should_alert('disk'):
                alerts.append({
                    'type': 'Disk',
                    'current': metrics['disk_percent'],
                    'thresholds': THRESHOLDS['disk_percent']

                })
                self.last_alert_time['disk'] = time.time()
        return alerts
    def _should_alert(self, metric_type):
        """Check if enough time has passed since last alert (prevents spam)"""
        if metric_type not in self.last_alert_time:
            return True
        
        time_since_last_alert = time.time() - self.last_alert_time[metric_type]
        return time_since_last_alert > MONITORING_CONFIG['alert_cooldown']
    
class AlertManager:
    """Manages alert notification"""

    @staticmethod
    def send_email_alert(server_name, metrics, alerts):
        """Send email alert for threshold breaches"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG['sender_email']
            msg['To'] = EMAIL_CONFIG['recipient_email']
            msg['Subject'] = f"🚨 ALERT: Health Issue on {server_name}"

            # Build email body
            body = f"""
HEALTH MONITORING ALERT
{'=' *60}


Server: {server_name}
Time: {metrics['timestamp']}
Status: CRITICAL

THRESHOLD BREACHES:
{'=' * 60}
"""
            for alert in alerts:
                body += f"""
{alert['type']}:
  Current Value: {alert['current']:.1f}%
  Threshold: {alert['thresholds']}%
  Status: ⚠️ EXCEEDED
"""
                body += f"""
{'='*60}

CURRENT METRICS:
CPU: {metrics['cpu_percent']:.1f}%
Memory: {metrics['memory_percent']:.1f}%
Disk: {metrics['disk_percent']:.1f}%
Uptime: {metrics['uptime']}

{'='*60}

This is an automated alert from your Health Monitoring System.
Please investigate the server immediately.
"""
                msg.attach(MIMEText(body, "plain"))

                #Send email
                server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
                server.starttls()
                server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
                server.send_message(msg)
                server.quit()

                print(f"✓ Email alert sent for {server_name}")
            
            # Log alert
            AlertManager.log_alert(server_name, alerts)
            
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email alert: {e}")
            return False
    

    @staticmethod
    def log_alert(server_name, alerts):
        """Log alert to file"""
        try:
            os.makedirs(MONITORING_CONFIG['log_directory'], exist_ok=True)
            
            with open(ALERT_LOG_FILE, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                alert_types = ', '.join([a['type'] for a in alerts])
                f.write(f"{timestamp} | {server_name} | {alert_types}\n")
                
        except Exception as e:
            print(f"✗ Failed to log alert: {e}")

class MetricsLogger:
    """Logs metrics to CSV file"""

    @staticmethod
    def log_metrics(metrics):
        """Append metrics to CSV file"""
        try:
            # Create log directory if it doesn't exist
            os.makedirs(MONITORING_CONFIG['log_directory'], exist_ok=True)

            # Check if file exists (for header)
            file_exists = os.path.exists(LOG_FILE)

            with open(LOG_FILE, 'a', newline= '') as f:
                fieldnames = ['timestamp', 'server_name', 'status', 'cpu_percent', 'memory_percent', 'disk_percent', 'uptime']
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                # Write header if new file
                if not file_exists:
                    writer.writeheader()

                # write metrics
                writer.writerow(metrics)
            return True
        
        except Exception as e:
            print(f"✗ Failed to log metrics: {e}")
            return False
        

class HealthMonitoringSystem:
    """Main monitoring system coordinator"""

    def __init__(self):
        self.monitors ={}

        # Create monitor for each server
        for name, config in SERVERS.items():
            self.monitors[name] = ServerMonitor(name, config)
        
        print(f"✓ Health Monitoring System initialized")
        print(f"  Monitoring {len(self.monitors)} server(s)")
        print(f"  Check interval: {MONITORING_CONFIG['check_interval']} seconds")
        print(f"  Thresholds: CPU>{THRESHOLDS['cpu_percent']}%, "
              f"Memory>{THRESHOLDS['memory_percent']}%, "
              f"Disk>{THRESHOLDS['disk_percent']}%")
        

    def check_all_servers(self):
        """Check health of all servers"""
        print(f"\n{'='*70}")
        print(f"Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        
        for name, monitor in self.monitors.items():
            print(f"\nChecking {name}...")
            
            # Collect metrics
            metrics = monitor.get_metrics()
            
            # Display metrics
            if metrics['status'] == 'healthy':
                print(f"  Status: ✓ Healthy")
                print(f"  CPU: {metrics['cpu_percent']:.1f}%")
                print(f"  Memory: {metrics['memory_percent']:.1f}%")
                print(f"  Disk: {metrics['disk_percent']:.1f}%")
                print(f"  Uptime: {metrics['uptime']}")
                
                # Check thresholds
                alerts = monitor.check_thresholds(metrics)
                
                if alerts:
                    print(f"  ⚠️ ALERTS:")
                    for alert in alerts:
                        print(f"    - {alert['type']}: {alert['current']:.1f}% "
                              f"(threshold: {alert['thresholds']}%)")
                    
                    # Send email alert
                    AlertManager.send_email_alert(name, metrics, alerts)
                
            else:
                print(f"  Status: ✗ {metrics['status']}")
            
            # Log metrics
            MetricsLogger.log_metrics(metrics)
        
        print(f"\n{'='*70}")            

    def run(self):
        """Run continuous monitoring loop"""
        print(f"\n🚀 Starting Health Monitoring System")
        print(f"Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.check_all_servers()
                
                print(f"\nNext check in {MONITORING_CONFIG['check_interval']} seconds...")
                time.sleep(MONITORING_CONFIG['check_interval'])
                
        except KeyboardInterrupt:
            print(f"\n\n✓ Monitoring stopped by user")
            print(f"Logs saved to: {LOG_FILE}")
            print(f"Alert log: {ALERT_LOG_FILE}")

# Main execution
if __name__ == "__main__":
    system = HealthMonitoringSystem()
    system.run()


        
        
