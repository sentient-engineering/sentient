import subprocess
from smolagents import tool

@tool
def firewall_guard() -> str:
    """Runs proactive scan and ensure firewall status via ufw."""
    try:
        status = subprocess.getoutput("sudo ufw status")
        if "inactive" in status.lower():
            subprocess.run("sudo ufw --force enable", shell=True, check=True)
            return "Firewall auto-reactivated."
        return "Firewall active."
    except Exception as e:
        return f"Firewall check failed: {e}"

@tool
def kernel_audit() -> str:
    """Audit and verify kernel security & performance parameters."""
    try:
        result = subprocess.getoutput("sysctl -a | grep -E 'vm.|net.|kernel.' | head -n 25")
        return f"Kernel parameter snapshot:\n{result}"
    except Exception as e:
        return f"Kernel audit failed: {e}"