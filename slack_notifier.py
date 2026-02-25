#!/usr/bin/env python3
"""
Slack Notification Module for Health Monitoring System
Sends real-time alerts to Slack channels when server thresholds are exceeded
"""

import json
import urllib.request
import urllib.error
from datetime import datetime

class SlackNotifier:
    """
    Handles Slack webhook notifications for server alerts
    
    Usage:
        notifier = SlackNotifier(webhook_url)
        notifier.send_alert(server_name, metrics, alerts)
    """
    
    def __init__(self, webhook_url):
        """
        Initialize Slack notifier
        
        Args:
            webhook_url (str): Slack incoming webhook URL
        """
        self.webhook_url = webhook_url
    
    def send_alert(self, server_name, metrics, alerts):
        """
        Send formatted alert to Slack channel
        
        Args:
            server_name (str): Name of the server with issues
            metrics (dict): Current metrics (cpu, memory, disk, uptime)
            alerts (list): List of threshold breaches
            
        Returns:
            bool: True if successful, False otherwise
        """
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Determine severity based on number of alerts
        if len(alerts) >= 3:
            severity_emoji = "🔴"  # Critical - multiple issues
            severity_text = "CRITICAL"
        elif len(alerts) >= 2:
            severity_emoji = "🟡"  # Warning - couple issues
            severity_text = "WARNING"
        else:
            severity_emoji = "🟠"  # Alert - single issue
            severity_text = "ALERT"
        
        # Build rich Slack message using Block Kit
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{severity_emoji} {severity_text}: {server_name}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Time:*\n{timestamp}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Server:*\n{server_name}"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
        
        # Add threshold breaches section
        alert_text = "*Threshold Breaches:*\n"
        for alert in alerts:
            alert_emoji = self._get_metric_emoji(alert['type'])
            alert_text += f"{alert_emoji} *{alert['type']}*: "
            alert_text += f"{alert['current']:.1f}% "
            alert_text += f"(limit: {alert['threshold']}%)\n"
        
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": alert_text
            }
        })
        
        # Add current metrics section
        metrics_text = "*Current Metrics:*\n"
        metrics_text += f"• CPU: {metrics.get('cpu_percent', 'N/A')}%\n"
        metrics_text += f"• Memory: {metrics.get('memory_percent', 'N/A')}%\n"
        metrics_text += f"• Disk: {metrics.get('disk_percent', 'N/A')}%\n"
        metrics_text += f"• Uptime: {metrics.get('uptime', 'N/A')}"
        
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": metrics_text
            }
        })
        
        # Add action footer
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "🤖 Automated alert from Health Monitoring System"
                }
            ]
        })
        
        # Prepare payload
        payload = {
            "text": f"{severity_text}: Health issue detected on {server_name}",
            "blocks": blocks
        }
        
        # Send to Slack
        return self._send_webhook(payload)
    
    def _send_webhook(self, payload):
        """
        Send webhook request to Slack
        
        Args:
            payload (dict): Slack message payload
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Convert payload to JSON
            data = json.dumps(payload).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            # Send request with timeout
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    print("✓ Slack notification sent successfully")
                    return True
                else:
                    print(f"✗ Slack notification failed: HTTP {response.status}")
                    return False
                    
        except urllib.error.HTTPError as e:
            print(f"✗ Slack HTTP error: {e.code} - {e.reason}")
            return False
            
        except urllib.error.URLError as e:
            print(f"✗ Slack URL error: {e.reason}")
            return False
            
        except Exception as e:
            print(f"✗ Slack notification error: {e}")
            return False
    
    def _get_metric_emoji(self, metric_type):
        """
        Get emoji for metric type
        
        Args:
            metric_type (str): Type of metric (CPU, Memory, Disk)
            
        Returns:
            str: Appropriate emoji
        """
        emojis = {
            'CPU': '⚡',
            'Memory': '💾',
            'Disk': '💿',
            'cpu': '⚡',
            'memory': '💾',
            'disk': '💿'
        }
        return emojis.get(metric_type, '⚠️')
    
    def test_connection(self):
        """
        Send test message to Slack to verify webhook works
        
        Returns:
            bool: True if successful, False otherwise
        """
        test_payload = {
            "text": "✅ Health Monitoring System - Slack Integration Test",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Health Monitoring System*\n\nSlack integration is working correctly! 🎉\n\nYou will receive alerts here when server thresholds are exceeded."
                    }
                }
            ]
        }
        
        print("Sending test message to Slack...")
        return self._send_webhook(test_payload)


# Test functionality (run only when executed directly)
if __name__ == "__main__":
    print("=" * 60)
    print("Slack Notifier Test Module")
    print("=" * 60)
    print("\nThis module provides Slack notification capabilities.")
    print("To test, update config.py with your webhook URL and run:")
    print("  python3 test_slack.py")
    print()