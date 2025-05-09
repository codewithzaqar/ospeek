import platform
import psutil
import datetime

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
    
    def get_disk_info(self):
        disk = psutil.disk_usage('/')
        return {
            "Total (GB)": disk.total / (1024**3),
            "Used (GB)": disk.used / (1024**3),
            "Free (GB)": disk.free / (1024**3),
            "Usage (%)": disk.percent,
        }
    
    def get_network_info(self):
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_io_counters(pernic=True)
        result = []
        for iface in interfaces:
            if iface in stats:
                ip = next((addr.address for addr in interfaces[iface] if addr.family == 2), "N/A")
                result.append({
                    "Interface": iface,
                    "IP Address": ip,
                    "Bytes Sent (MB)": stats[iface].bytes_sent / (1024**2),
                    "Bytes Received (MB)": stats[iface].bytes_recv / (1024**2),
                })
        return result
    
    def get_process_info(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                processes.append({
                    "PID": proc.info['pid'],
                    "Name": proc.info['name'],
                    "CPU (%)": proc.info['cpu_percent'],
                    "Memory (MB)": proc.info['memory_info'].rss / (1024**2),
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return sorted(processes, key=lambda x: x["CPU (%)"], reverse=True)[:10]

    def get_uptime_info(self):
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime_seconds = (datetime.datetime.now() - boot_time).total_seconds()
        days = int(uptime_seconds // (24 * 3600))
        hours = int((uptime_seconds % (24 * 3600)) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        uptime_str = f"{days} days, {hours} hours, {minutes} minutes"
        return {
            "Uptime": uptime_str,
            "Boot Time": boot_time.strftime("%Y-%m-%d %H:%M:%S")
        }