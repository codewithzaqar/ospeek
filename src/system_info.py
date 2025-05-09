import platform
import psutil
import datetime
import sys

class SystemInfo:
    def get_system_info(self, verbose=False):
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
        if verbose:
            info["system"]["Platform"] = platform.platform()
            info["system"]["Python Version"] = sys.version.split()[0]
        return info
    
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
    
    def get_process_info(self, verbose=False, sort_key="cpu", filter_val=None):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status', 'username']):
            try:
                proc_info = {
                    "PID": proc.info['pid'],
                    "Name": proc.info['name'],
                    "CPU (%)": proc.info['cpu_percent'],
                    "Memory (MB)": proc.info['memory_info'].rss / (1024**2),
                }
                if verbose:
                    proc_info["Status"] = proc.info['status']
                    proc_info["User"] = proc.info['username']
                if filter_val:
                    if filter_val.isdigit() and int(filter_val) != proc_info["PID"]:
                        continue
                    elif filter_val.lower() not in proc_info["Name"].lower():
                        continue
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if sort_key == "cpu":
            return sorted(processes, key=lambda x: x["CPU (%)"], reverse=True)[:10]
        elif sort_key == "memory":
            return sorted(processes, key=lambda x: x["Memory (MB)"], reverse=True)[:10]
        elif sort_key == "pid":
            return sorted(processes, key=lambda x: x["PID"])[:10]
        return processes[:10] if processes else [{"Status": "No matching processes found"}]

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
    
    def get_user_info(self, verbose=False):
        users = []
        for user in psutil.users():
            user_info = {
                "Username": user.name,
                "Terminal": user.terminal or "N/A",
                "Host": user.host or "localhost",
                "Logic Time": datetime.datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")
            }
            if verbose:
                user_info["PID"] = user.pid if user.pid else "N/A"
            users.append(user_info)
        return users
    
    def get_battery_info(self):
        battery = psutil.sensors_battery()
        if battery is None:
            return {"Status": "No battery detected"}
        time_remaining = "N/A"
        if battery.secsleft and battery.secsleft != psutil.POWER_TIME_UNLIMITED:
            hours = battery.secsleft // 3600
            minutes = (battery.secsleft % 3600) // 60
            time_remaining = f"{int(hours)} hours, {int(minutes)} minutes"
        return {
            "Percentage (%)": battery.percent,
            "Power Plugged": bool(battery.power_plugged),
            "Time Remaining": time_remaining
        }
    
    def get_temperature_info(self):
        result = []
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures() or {}
                for sensor, readings in temps.items():
                    for reading in readings:
                        temp_info = {
                            "Sensor": f"{sensor} ({reading.label or 'default'})",
                            "Current (°C)": reading.current,
                            "High (°C)": reading.high if reading.high else "N/A",
                            "Critical (°C)": reading.critical if reading.critical else "N/A"
                        }
                        result.append(temp_info)
        except Exception as e:
            return [{"Status": f"Error retrieving temperature data: {str(e)}"}]
        return result if result else [{"Status": "No temperature sensors detected"}]
    
    def get_fan_info(self):
        fans = psutil.sensors_fans() if hasattr(psutil, 'sensors_fans') else {}
        result = []
        try:
            for fan, readings in fans.items():
                for reading in readings:
                    fan_info = {
                        "Fan": f"{fan} ({reading.label or 'default'})",
                        "Speed (RPM)": reading.current
                    }
                    result.append(fan_info)
        except Exception as e:
            return [{"Status": f"Error retrieving fan data: {str(e)}"}]
        return result if result else [{"Status": "No fan sensors detected"}]