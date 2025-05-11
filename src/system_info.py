import platform
import psutil
import datetime
import sys
import os
import time

try:
    import win32evtlog # type: ignore
except ImportError:
    win32evtlog = None

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
    
    def get_service_info(self):
        services = []
        try:
            if hasattr(psutil, 'win_service_iter') and platform.system() == "Windows":
                for service in psutil.win_service_iter():
                    try:
                        svc = service.as_dict()
                        services.append({
                            "Service": svc["name"],
                            "Status": svc["status"],
                            "PID": svc["pid"] if svc["pid"] else "N/A"
                        })
                    except psutil.NoSuchProcess:
                        continue
            else:
                # On Unix-like systems, simulate service info using known daemons
                known_services = ["sshd", "cron", "apache2", "nginx", "mysql"]
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        name = proc.info['name'].lower()
                        for svc in known_services:
                            if svc in name:
                                services.append({
                                    "Service": svc,
                                    "Status": "running",
                                    "PID": proc.info['pid']
                                })
                                break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                # Add stopped services for known services not found
                found_services = {svc["Service"] for svc in services}
                for svc in known_services:
                    if svc not in found_services:
                        services.append({
                            "Service": svc,
                            "Status": "stopped",
                            "PID": "N/A"
                        })
        except Exception as e:
            return [{"Status": f"Error retrieving service data: {str(e)}"}]
        return services if services else [{"Status": "No services detected"}]
    
    def get_log_info(self):
        logs = []
        try:
            if platform.system() == "Windows" and win32evtlog:
                server = None  # Local machine
                log_type = "System"
                hand = win32evtlog.OpenEventLog(server, log_type)
                flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
                events = win32evtlog.ReadEventLog(hand, flags, 0)
                for event in events[:50]:  # Limit to 50 to avoid excessive data
                    timestamp = event.TimeGenerated.strftime("%Y-%m-%d %H:%M:%S")
                    source = event.SourceName
                    message = str(event.StringInserts) if event.StringInserts else "N/A"
                    logs.append({
                        "Timestamp": timestamp,
                        "Source": source,
                        "Message": message
                    })
                win32evtlog.CloseEventLog(hand)
            else:
                log_files = ["/var/log/syslog", "/var/log/messages"]
                for log_file in log_files:
                    if os.path.exists(log_file):
                        with open(log_file, "r", errors="ignore") as f:
                            lines = f.readlines()[-50:]  # Last 50 lines
                            for line in lines:
                                parts = line.split(" ", 5)
                                if len(parts) >= 5:
                                    timestamp = f"{parts[0]} {parts[1]} {parts[2]}"
                                    source = parts[4].split(":")[0]
                                    message = parts[5].strip()
                                    logs.append({
                                        "Timestamp": timestamp,
                                        "Source": source,
                                        "Message": message
                                    })
                        break
        except Exception as e:
            return [{"Status": f"Error retrieving log data: {str(e)}"}]
        return logs if logs else [{"Status": "No log entries found"}]
    
    def get_alert_info(self, thresholds):
        alerts = []
        try:
            # CPU Usage
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_status = "ALERT" if cpu_usage > thresholds["cpu"] else "OK"
            alerts.append({
                "Metric": "CPU Usage",
                "Current (%)": cpu_usage,
                "Threshold (%)": thresholds["cpu"],
                "Status": cpu_status
            })

            # Memory Usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            memory_status = "ALERT" if memory_usage > thresholds["memory"] else "OK"
            alerts.append({
                "Metric": "Memory Usage",
                "Current (%)": memory_usage,
                "Threshold (%)": thresholds["memory"],
                "Status": memory_status
            })

            # Disk Usage
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent
            disk_status = "ALERT" if disk > thresholds["disk"] else "OK"
            alerts.append({
                "Metric": "Disk Usage",
                "Current (%)": disk_usage,
                "Threshold (%)": thresholds["disk"],
                "Status": disk_status 
            })
        except Exception as e:
            return [{"Status": f"Error retrieving alert data: {str(e)}"}]
        return alerts
    
    def get_network_stats(self):
        stats = []
        try:
            initial_stats = psutil.net_io_counters(pernic=True)
            time.sleep(1)  # Wait to calculate bandwidth
            final_stats = psutil.net_io_counters(pernic=True)
            for iface in initial_stats:
                initial = initial_stats[iface]
                final = final_stats.get(iface, initial)
                bandwidth_sent = (final.bytes_sent - initial.bytes_sent) / (1024**2)  # MB/s
                bandwidth_recv = (final.bytes_recv - initial.bytes_recv) / (1024**2)  # MB/s
                stats.append({
                    "Interface": iface,
                    "Packets Sent": final.packets_sent,
                    "Packets Received": final.packets_recv,
                    "Errors In": final.errin,
                    "Errors Out": final.errout,
                    "Dropped Packets": final.dropout + final.dropin,
                    "Bandwidth Sent (MB/s)": bandwidth_sent,
                    "Bandwidth Received (MB/s)": bandwidth_recv
                })
        except Exception as e:
            return [{"Status": f"Error retrieving network stats: {str(e)}"}]
        return stats if stats else [{"Status": "No network interfaces detected"}]