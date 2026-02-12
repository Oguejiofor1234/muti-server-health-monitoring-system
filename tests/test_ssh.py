from config import SERVERS
import paramiko

for name, config in SERVERS.items():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(**config, timeout=10)
        print(f"✓ {name}: Connected")
        client.close()
    except Exception as e:
        print(f"✗ {name}: Failed - {e}")
