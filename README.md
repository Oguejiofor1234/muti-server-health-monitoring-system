# 🏥 Remote Multi-Server Health Monitoring System

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/YOUR-USERNAME/health-monitoring-system/graphs/commit-activity)

> Automated health monitoring system that tracks CPU, memory, and disk usage across multiple servers via SSH and sends real-time email alerts when thresholds are breached.

![Demo Screenshot](screenshots/demo.png)

## 🎯 Overview

This project implements a distributed server monitoring solution designed for DevOps environments. It continuously monitors critical system resources on remote servers, detects anomalies, and automatically notifies administrators via email when predefined thresholds are exceeded.

### The Problem

In production environments, server issues often go unnoticed until users report problems. Manual monitoring is time-consuming and doesn't scale. Without automated alerts, critical resource exhaustion (disk full, memory leak, CPU spike) can cause unexpected downtime.

### The Solution

An automated monitoring system that:
- ✅ Monitors multiple servers remotely via SSH (no agent installation)
- ✅ Tracks CPU, memory, disk, and uptime in real-time
- ✅ Sends instant email alerts when thresholds are breached
- ✅ Logs all metrics to CSV for historical analysis
- ✅ Prevents alert spam with intelligent cooldown periods
- ✅ Handles server failures gracefully

---

## 🚀 Features

- **Multi-Server Monitoring**: Track unlimited servers from a single control point
- **Real-Time Alerts**: Instant email notifications when issues detected
- **Threshold-Based**: Configurable limits (CPU > 75%, Memory > 85%, Disk > 90%)
- **Historical Logging**: All metrics saved to CSV for trend analysis
- **Zero-Agent Architecture**: No software installation on monitored servers
- **Production-Ready**: Error handling, retry logic, and graceful degradation
- **Scalable**: Easily add more servers by updating configuration

---

## 📊 Architecture

### System Design


### Data Flow

```
1. Connect → SSH to each server
2. Collect → Execute psutil commands remotely
3. Analyze → Compare metrics vs thresholds
4. Alert → Send email if threshold breached
5. Log → Save all data to CSV
6. Repeat → Every 60 seconds (configurable)
```

---

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Paramiko** | SSH client for remote connections |
| **psutil** | System metrics collection |
| **smtplib** | Email alert delivery |
| **CSV** | Data logging and storage |
| **Vagrant** | VM management (testing) |

---

## 📋 Prerequisites

### Required Software

- Python 3.8 or higher
- SSH access to servers you want to monitor
- Gmail account (for email alerts)

### Required Python Packages
```bash
pip install paramiko psutil
```
