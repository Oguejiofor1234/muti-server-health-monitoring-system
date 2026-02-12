''' Configuration  file for Health Monitoring System'''
import os
# Server Configuration
SERVERS = {
    'web-server':{
        'hostname': '127.0.0.1',   # Update with your VM's IP
        'port': 22,  # Update with your port
        'username': 'your-username', # Update with your username
        'key_filename': os.path.expanduser('~/.ssh/monitoring_key')  # Update with your key
    },
    'database': {
        'hostname': '127.0.0.1',    # Update as in web-server
        'port': 20,
        'username': 'your-username',
        'key_filename': os.path.expanduser('~/.ssh/monitoring_key')
    }    
}

#  Monitoring Thresholds
THRESHOLDS = {
    'cpu_percent':75,     # Alert if CPU >75%
    'memory_percent': 85, # Alert if Memory > 85%
    'disk_percent': 90    # Amert if Disk >90%
}
# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',
    'sender_password': 'your-app-password',  # Gmail App Password
    'recipient_email': 'alerts@example.com'

}
# Monitoring configuration
MONITORING_CONFIG = {
    'check_interval': 60,           # Check every 60 seconds
    'alert_cooldown': 300,          # Don't re-alert for same issue within 5 minutes
    'log_directory': './logs',      # Where to store log files
    'max_retries': 3                # Retry failed connections 3 times

}

# File Paths
LOG_FILE = os.path.join(MONITORING_CONFIG['log_directory'], 'health_metrics.csv')
ALERT_LOG_FILE = os.path.join(MONITORING_CONFIG['log_directory'], 'alerts.log')