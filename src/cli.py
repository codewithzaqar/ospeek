import argparse
import time
from .system_info import SystemInfo
from .utils import print_formatted, print_process_table, print_json, clear_screen, send_notification

class OSPeekCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="OSPeek CLI v0.1.5")
        self.parser.add_argument(
            "command",
            choices=["info", "disk", "network", "processes", "uptime", "users", "battery", "temperature", "fan", "services", "logs", "alerts", "network-stats", "summary", "version", "help"],
            help="Command to execute",
            nargs="?",
            default="help",
        )
        self.parser.add_argument(
            "--json",
            action="store_true",
            help="Output results in JSON format",
        )
        self.parser.add_argument(
            "--verbose",
            action="store_true",
            help="Display additional details (for info, processes, users)",
        )
        self.parser.add_argument(
            "--sort",
            choices=["cpu", "memory", "pid"],
            default="cpu",
            help="Sort processes by cpu, memory, or pid (for processes command)",
        )
        self.parser.add_argument(
            "--refresh",
            type=float,
            default=0,
            help="Refresh output every N seconds (for processes, users)",
        )
        self.parser.add_argument(
            "--filter",
            help="Filrer processes by name or PID (for processes command)",
        )
        self.parser.add_argument(
            "--watch",
            type=float,
            default=0,
            help="Watch output every N seconds (for temperature, fan)"
        )
        self.parser.add_argument(
            "--count",
            type=int,
            default=0,
            help="Limit number of entries displayed  (for logs, services; default 10 for logs)",
        )
        self.parser.add_argument(
            "--threshold",
            help="Set alert thresholds as cpu,memory,disk (e.g., cpu=80,memory=85,disk=90) (for alerts command)",
        )
        self.parser.add_argument(
            "--notify",
            action="store_true",
            help="Send desktop notifications for alerts (requires plyer)",
        )

    def run(self, args):
        args = self.parser.parse_args(args)
        if args.command == "info":
            self.show_info(args.json, args.verbose)
        elif args.command == "disk":
            self.show_disk(args.json)
        elif args.command == "network":
            self.show_network(args.json)
        elif args.command == "processes":
            self.show_processes(args.json, args.verbose, args.sort, args.refresh)
        elif args.command == "uptime":
            self.show_uptime(args.json)
        elif args.command == "users":
            self.show_users(args.json, args.verbose, args.refresh)
        elif args.command == "battery":
            self.show_battery(args.json)
        elif args.command == "temperature":
            self.show_temperature(args.json, args.watch)
        elif args.command == "fan":
            self.show_fan(args.json, args.watch)
        elif args.command == "services":
            self.show_services(args.json, args.count)
        elif args.command == "logs":
            self.show_logs(args.json, args.count)
        elif args.command == "alerts":
            self.show_alerts(args.json, args.watch, args.threshold)
        elif args.command == "network-stats":
            self.show_network_stats(args.json, args.watch)
        elif args.command == "summary":
            self.show_summary(args.json, args.watch)
        elif args.command == "version":
            self.show_version(args.json)
        else:
            self.show_help()

    def show_info(self, json_output, verbose):
        sys_info = SystemInfo()
        info = sys_info.get_system_info(verbose)
        if json_output:
            print_json(info)
        else:
            print_formatted("System Information", info["system"])
            print_formatted("CPU Information", info["cpu"])
            print_formatted("Memory Information", info["memory"])

    def show_disk(self, json_output):
        sys_info = SystemInfo()
        disk_info = sys_info.get_disk_info()
        if json_output:
            print_json(disk_info)
        else:
            print_formatted("Disk Usage", disk_info)

    def show_network(self, json_output):
        sys_info = SystemInfo()
        network_info = sys_info.get_network_info()
        if json_output:
            print_json(network_info)
        else:
            for interface in network_info:
                print_formatted(f"Interface: {interface['Interface']}", interface)

    def show_processes(self, json_output, verbose, sort_key, refresh):
        sys_info = SystemInfo()
        if refresh > 0 and not json_output:
            try:
                while True:
                    clear_screen()
                    process_info = sys_info.get_process_info(verbose, sort_key)
                    print_process_table("Running Processes", process_info, verbose)
                    print(f"[Refreshes every {refresh} second{'s' if refresh != 1 else ''}, press Ctrl+C to stop]")
                    time.sleep(refresh)
            except KeyboardInterrupt:
                print("\nStopped refreshing")
        else:
            process_info = sys_info.get_process_info(verbose, sort_key)
            if json_output:
                print_json(process_info)
            else:
                print_process_table("Running Processes", process_info, verbose)

    def show_uptime(self, json_output):
        sys_info = SystemInfo()
        uptime_info = sys_info.get_uptime_info()
        if json_output:
            print_json(uptime_info)
        else:
            print_formatted("System Uptime", uptime_info)

    def show_users(self, json_output, verbose, refresh):
        sys_info = SystemInfo()
        if refresh > 0 and not json_output:
            try:
                while True:
                    clear_screen()
                    user_info = sys_info.get_user_info(verbose)
                    for user in user_info:
                        print_formatted(f"Username: {user['Username']}", user)
                    print(f"[Refreshes every {refresh} second{'s' if refresh != 1 else ''}, press Ctrl+C to stop]")
                    time.sleep(refresh)
            except KeyboardInterrupt:
                print("\nStopped refreshing")
        else:
            user_info = sys_info.get_user_info(verbose)
            if json_output:
                print_json(user_info)
            else:
                for user in user_info:
                    print_formatted(f"Username: {user['Username']}", user)

    def show_battery(self, json_output):
        sys_info = SystemInfo()
        battery_info = sys_info.get_battery_info()
        if json_output:
            print_json(battery_info)
        else:
            print_formatted("Battery Status", battery_info)

    def show_temperature(self, json_output, watch):
        sys_info = SystemInfo()
        if watch > 0 and not json_output:
            try:
                while True:
                    clear_screen()
                    temp_info = sys_info.get_temperature_info()
                    if temp_info and "Status" in temp_info[0]:
                        print_formatted("Temperature Sensors", temp_info[0])
                    else:
                        for sensor in temp_info:
                            print_formatted(f"Sensor: {sensor['Sensor']}", sensor)
                    print(f"[Refreshes every {watch} second{'s' if watch != 1 else ''}, press Ctrl+C to stop]")
                    time.sleep(watch)
            except KeyboardInterrupt:
                print("\nStopped refreshing")
        else:
            temp_info = sys_info.get_temperature_info()
            if json_output:
                print_json(temp_info)
            else:
                if temp_info and "Status" in temp_info[0]:
                    print_formatted("Temperature Sensors", temp_info[0])
                else:
                    for sensor in temp_info:
                        print_formatted(f"Sensor: {sensor['Sensor']}", sensor)

    def show_fan(self, json_output, watch):
        sys_info = SystemInfo()
        if watch > 0 and not json_output:
            try:
                while True:
                    clear_screen()
                    fan_info = sys_info.get_fan_info()
                    if fan_info and "Status" in fan_info[0]:
                        print_formatted("Fan Speeds", fan_info[0])
                    else:
                        for fan in fan_info:
                            print_formatted(f"Fan: {fan['Fan']}", fan)
                    print(f"[Refreshes every {watch} second{'s' if watch != 1 else ''}, press Ctrl+C to stop]")
                    time.sleep(watch)
            except KeyboardInterrupt:
                print("\nStopped refreshing")
        else:
            fan_info = sys_info.get_fan_info()
            if json_output:
                print_json(fan_info)
            else:
                if fan_info and 'Status' in fan_info[0]:
                    print_formatted("Fan Speeds", fan_info[0])
                else:
                    for fan in fan_info:
                        print_formatted(f"Fan: {fan['Fan']}", fan)

    def show_services(self, json_output, count):
        sys_info = SystemInfo()
        service_info = sys_info.get_service_info()
        if count > 0:
            service_info = service_info[:count]
        if json_output:
            print_json(service_info)
        else:
            if service_info and "Status" in service_info[0]:
                print_formatted("System Services", service_info[0])
            else:
                for service in service_info:
                    print_formatted(f"Service: {service['Service']}", service)

    def show_logs(self, json_output, count):
        sys_info = SystemInfo()
        log_info = sys_info.get_log_info()
        if count > 0:
            log_info = log_info[:count]
        else:
            log_info = log_info[:10]  # Default limit for logs
        if json_output:
            print_json(log_info)
        else:
            if log_info and "Status" in log_info[0]:
                print_formatted("System Logs", log_info[0])
            else:
                for log in log_info:
                    print_formatted(f"Timestamp: {log['Timestamp']}", log)

    def show_alerts(self, json_output, watch, threshold):
        sys_info = SystemInfo()
        thresholds = self.parse_thresholds(threshold)
        if watch > 0 and not json_output:
            try:
                while True:
                    clear_screen()
                    alert_info = sys_info.get_alert_info(thresholds)
                    if alert_info and "Status" in alert_info[0]:
                        print_formatted("System Alerts", alert_info[0])
                    else:
                        for alert in alert_info:
                            print_formatted(f"Metric: {alert['Metric']}", alert)
                    print(f"[Refreshes every {watch} second{'s' if watch != 1 else ''}, press Ctrl+C to stop]")
                    time.sleep(watch)
            except KeyboardInterrupt:
                print("\nStopped refreshing")
        else:
            alert_info = sys_info.get_alert_info(thresholds)
            if json_output:
                print_json(alert_info)
            else:
                if alert_info and "Status" in alert_info[0]:
                    print_formatted("System Alerts", alert_info[0])
                else:
                    for alert in alert_info:
                        print_formatted(f"Metric: {alert['Metric']}", alert)

    def show_network_stats(self, json_output, watch):
        sys_info = SystemInfo()
        if watch > 0 and not json_output:
            try:
                while True:
                    clear_screen()
                    stats_info = sys_info.get_network_stats()
                    if stats_info and "Stats" in stats_info[0]:
                        print_formatted("Network Statistics", stats_info[0])
                    else:
                        for stats in stats_info:
                            print_formatted(f"Interface: {stats['Interface']}", stats)
                    print(f"[Refreshes every {watch} second{'s' if watch != 1 else ''}, press Ctrl+C to stop]")
                    time.sleep(watch)
            except KeyboardInterrupt:
                print("\nStopped refreshing")
        else:
            stats_info = sys_info.get_network_stats()
            if json_output:
                print_json(stats_info)
            else:
                if stats_info and "Status" in stats_info[0]:
                    print_formatted("Network Statistics", stats_info[0])
                else:
                    for stats in stats_info:
                        print_formatted(f"Interface: {stats['Interface']}", stats)

    def show_summary(self, json_output, watch):
        sys_info = SystemInfo()
        if watch > 0 and not json_output:
            try:
                while True:
                    clear_screen()
                    summary_info = sys_info.get_summery_info()
                    if summary_info.get("Status"):
                        print_formatted("System Summary", {"Status": summary_info["Status"]})
                    else:
                        print_formatted("System Summary", summary_info)
                    print(f"[Refreshes every {watch} second{'s' if watch != 1 else ''}, press Ctrl+C to stop]")
                    time.sleep(watch)
            except KeyboardInterrupt:
                print("\nStopped refreshing")
        else:
            summary_info = sys_info.get_summery_info()
            if json_output:
                print_json(summary_info)
            else:
                if summary_info.get("Status"):
                    print_formatted("System Summary", {"Status": summary_info["Status"]})
                else:
                    print_formatted("System Summary", summary_info)

    def parse_thresholds(self, threshold_str):
        defaults = {"cpu": 80.0, "memory": 85.0, "disk": 90.0}
        if threshold_str:
            try:
                for part in threshold_str.split(","):
                    key, value = part.split("=")
                    if key in defaults:
                        defaults[key] = float(value)
            except (ValueError, KeyError):
                print(f"Invalid threshold format: {threshold_str}. Using defaults.")
        return defaults

    def show_version(self, json_output):
        from . import __version__
        version_info = {"OSPeek CLI": f"v{__version__}"}
        if json_output:
            print_json(version_info)
        else:
            print_formatted("Version", version_info)

    def show_help(self):
        self.parser.print_help()