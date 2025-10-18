import subprocess
from smolagents import tool
from helium import go_to

@tool
def sys_optimize(param: str, value: str) -> str:
    """Apply safe sysctl optimization with verification."""
    try:
        subprocess.run(f"sudo sysctl -w {param}={value}", shell=True, check=True)
        return f"⚙️ Kernel parameter {param} set to {value}"
    except subprocess.CalledProcessError as e:
        return f"Error setting kernel parameter: {e}"

@tool
def manage_service(service: str, action: str) -> str:
    """Manage systemd services with logging."""
    try:
        subprocess.run(f"sudo systemctl {action} {service}", shell=True, check=True)
        return f"Service {service} {action} executed."
    except subprocess.CalledProcessError as e:
        return f"Error managing service {service}: {e}"

@tool
def launch_app(app: str) -> str:
    """Launch local applications or browser tabs."""
    if app.startswith("http"):
        try:
            go_to(app)
            return f"Opened {app}"
        except Exception as e:
            return f"Error opening URL: {e}"
    try:
        subprocess.Popen(app.split())
        return f"Launched {app}"
    except Exception as e:
        return f"Error launching application: {e}"

@tool
def read_pdf(path: str) -> str:
    """Extract text from stored PDF or image."""
    try:
        import PyPDF2
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join([p.extract_text() for p in reader.pages])
    except Exception as e:
        return f"Error reading PDF: {e}"