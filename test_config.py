#!/usr/bin/env python3
"""
ServerWatch Configuration Test
Author: xXLuckyGamer04Xx
Version: 1.0.0

Testet ob alle Konfigurationen korrekt sind
"""

import sys
import json
from pathlib import Path

# Farben
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_mark(status):
    return f"{GREEN}✓{RESET}" if status else f"{RED}✗{RESET}"

print("=" * 60)
print("ServerWatch Configuration Test")
print("=" * 60)
print()

# 1. Python Version
print("1. Python Version Check")
import sys
version = sys.version_info
if version >= (3, 9):
    print(f"   {check_mark(True)} Python {version.major}.{version.minor}.{version.micro}")
else:
    print(f"   {check_mark(False)} Python {version.major}.{version.minor} (3.9+ required)")
    sys.exit(1)

# 2. Dependencies
print("\n2. Dependencies Check")
deps = {
    'aiohttp': False,
    'mcstatus': False,
    'docker': False,
    'fastapi': False,
    'uvicorn': False,
}

for dep in deps:
    try:
        __import__(dep)
        deps[dep] = True
        print(f"   {check_mark(True)} {dep}")
    except ImportError:
        print(f"   {check_mark(False)} {dep} - pip install {dep}")

# 3. Config Files
print("\n3. Configuration Files")

# .env
env_exists = Path('.env').exists()
print(f"   {check_mark(env_exists)} .env file")

if env_exists:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    required_vars = [
        'DISCORD_WEBHOOK_URL',
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID',
        'DOCKER_HOST',
        'VSERVER_IP'
    ]
    
    for var in required_vars:
        value = os.getenv(var, '')
        has_value = bool(value and value != 'YOUR_' and value != '123.')
        print(f"   {check_mark(has_value)} {var}")

# servers.json
config_path = Path('config/servers.json')
config_exists = config_path.exists()
print(f"\n   {check_mark(config_exists)} config/servers.json")

if config_exists:
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        print(f"   {check_mark(True)} Valid JSON")
        print(f"   {check_mark(True)} {len(config.get('targets', []))} targets configured")
    except Exception as e:
        print(f"   {check_mark(False)} JSON parse error: {e}")

# 4. Directories
print("\n4. Directory Structure")
dirs = ['logs', 'dashboard', 'src/checks']
for d in dirs:
    exists = Path(d).exists()
    print(f"   {check_mark(exists)} {d}/")

# 5. Dashboard Files
print("\n5. Dashboard Files")
dashboard_files = ['dashboard/index.html', 'dashboard/style.css', 'dashboard/app.js']
for f in dashboard_files:
    exists = Path(f).exists()
    print(f"   {check_mark(exists)} {f}")

# 6. Check Modules
print("\n6. Check Modules")
check_modules = [
    'src/checks/ping_check.py',
    'src/checks/tcp_check.py',
    'src/checks/minecraft_check.py',
    'src/checks/docker_check.py'
]
for m in check_modules:
    exists = Path(m).exists()
    print(f"   {check_mark(exists)} {m}")

# 7. Core Modules
print("\n7. Core Modules")
core_modules = [
    'src/monitor.py',
    'src/history.py',
    'src/alerting.py',
    'src/notifier_discord.py',
    'src/notifier_telegram.py',
    'src/api.py'
]
for m in core_modules:
    exists = Path(m).exists()
    print(f"   {check_mark(exists)} {m}")

# Fazit
print("\n" + "=" * 60)

all_deps = all(deps.values())
all_configs = env_exists and config_exists

if all_deps and all_configs:
    print(f"{GREEN}✓ Alle Checks bestanden!{RESET}")
    print("\nDu kannst jetzt starten mit:")
    print("  python3 main.py")
else:
    print(f"{YELLOW}⚠ Einige Checks fehlgeschlagen{RESET}")
    print("\nBitte behebe die Fehler und führe diesen Test erneut aus:")
    print("  python3 test_config.py")

print("=" * 60)
