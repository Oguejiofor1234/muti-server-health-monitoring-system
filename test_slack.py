#!/usr/bin/env python3
"""
Test script for Slack notification integration
"""

from slack_notifier import SlackNotifier
from config import SLACK_CONFIG

def test_slack_notification():
    """Test Slack webhook connection"""
    
    print("=" * 60)
    print("Testing Slack Notification Integration")
    print("=" * 60)
    
    # Check if Slack is configured
    if not SLACK_CONFIG['enabled']:
        print("\n⚠️  Slack is disabled in config.py")
        print("To enable:")
        print("1. Set SLACK_CONFIG['enabled'] = True")
        print("2. Add your webhook URL")
        return
    
    webhook_url = SLACK_CONFIG['webhook_url']
    
    if 'YOUR/WEBHOOK/URL' in webhook_url:
        print("\n✗ Please update webhook_url in config.py with your actual Slack webhook")
        print("\nTo get a webhook URL:")
        print("1. Go to https://api.slack.com/apps")
        print("2. Create a new app or select existing")
        print("3. Enable 'Incoming Webhooks'")
        print("4. Create webhook for your channel")
        print("5. Copy the webhook URL to config.py")
        return
    
    # Initialize notifier
    notifier = SlackNotifier(webhook_url)
    
    # Send test message
    print("\nSending test message to Slack...\n")
    success = notifier.test_connection()
    
    if success:
        print("\n✅ SUCCESS! Check your Slack channel for the test message.")
    else:
        print("\n✗ FAILED! Check your webhook URL and Slack configuration.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_slack_notification()