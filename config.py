''' Configuration  file for Health Monitoring System'''
import os
# Server Configuration
SERVERS = {
    'web-server':{
        'hostname': '127.0.0.1',   # Update with your VM's IP
        'port': 2222,  # Update with your port
        'username': 'vagrant', # Update with your username
        'key_filename': os.path.expanduser('~/.ssh/vm_key')  # Update with your key
    },
    'database': {
        'hostname': '127.0.0.1',    # Update as in web-server
        'port': 2200,
        'username': 'vagrant',
        'key_filename': os.path.expanduser('~/.ssh/vm_key')
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
    'enabled': True,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'miracle2cool247@gmail.com',
    'sender_password': 'xcxh aedo bzlw egmm',  # Gmail App Password
    'recipient_email': 'oguejiofor.mbah@fuoye.edu.ng'

}

# Slack Configuration (NEW - Slack Notification Feature!)
SLACK_CONFIG = {
    'enabled': True,  # Set to True to enable Slack notifications
    'webhook_url': 'YOUR/WEBHOOT/URL',
    'send_email_also': True  # If True, sends both email and Slack
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