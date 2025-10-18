import os
import subprocess
import time
from threading import Thread

def defense_loop():
    """Continuously monitor and enforce firewall rules."""
    while True:
        try:
            out = subprocess.run("sudo iptables -L", shell=True, capture_output=True, text=True)
            if "DROP" not in out.stdout:
                subprocess.run("sudo ufw enable; sudo ufw default deny incoming", shell=True)
        except Exception as e:
            # Log error, but continue running
            print(f"Defense loop error: {e}")
        time.sleep(120)

def optimizer_loop():
    """Periodically check CPU usage and adjust swappiness if needed."""
    while True:
        try:
            cpu_usage_str = os.popen("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'").read()
            if cpu_usage_str:
                cpu = float(cpu_usage_str)
                if cpu > 80:
                    subprocess.run("sudo sysctl -w vm.swappiness=10", shell=True)
        except (ValueError, IndexError) as e:
            print(f"Optimizer loop error reading CPU stats: {e}")
        except Exception as e:
            print(f"Optimizer loop error: {e}")
        time.sleep(300)

def start_proactive_agents():
    """Initialize and start the proactive defense and optimizer agents in separate threads."""
    defense_thread = Thread(target=defense_loop, daemon=True)
    optimizer_thread = Thread(target=optimizer_loop, daemon=True)
    defense_thread.start()
    optimizer_thread.start()
    print("🛡️ Proactive defense and optimization agents are active.")