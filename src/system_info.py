import platform
import psutil

class SystemInfo:
    def get_system_info(self):
        return {
            "system": {
                "OS": platform.system(),
                "OS Version": platform.release(),
                "Architecture": platform.machine(),
                "Node Name": platform.node(),
            },
            "cpu": {
                "Processor": platform.processor(),
                "Cores": psutil.cpu_count(logical=False),
                "Logical Cores": psutil.cpu_count(logical=True),
                "Usage (%)": psutil.cpu_percent(interval=1),
                "Frequency (MHz)": psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
            },
            "memory": {
                "Total (GB)": psutil.virtual_memory().total / (1024**3),
                "Available (GB)": psutil.virtual_memory().available / (1024**3),
                "Used (GB)": psutil.virtual_memory().used / (1024**3),
                "Usage (%)": psutil.virtual_memory().percent,
            }
        }