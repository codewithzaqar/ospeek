import argparse
from .system_info import SystemInfo
from .utils import print_formatted, print_process_table, print_json

class OSPeekCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="OSPeek CLI v0.0.7")
        self.parser.add_argument(
            "command",
            choices=["info", "disk", "network", "processes", "uptime", "users", "version", "help"],
            help="Command to execute",
            nargs="?",
            default="help",
        )
        self.parser.add_argument(
            "--json",
            action="store_true",
            help="Output results in JSON format"
        )
        self.parser.add_argument(
            "--verbose",
            action="store_true",
            help="Display additional details (for info, processes, users)"
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
            self.show_processes(args.json, args.verbose)
        elif args.command == "uptime":
            self.show_uptime(args.json)
        elif args.command == "users":
            self.show_users(args.json, args.verbose)
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

    def show_processes(self, json_output, verbose):
        sys_info = SystemInfo()
        process_info = sys_info.get_process_info(verbose)
        if json_output:
            print_json(process_info)
        else:
            print_process_table("Running Processes", process_info)

    def show_uptime(self, json_output):
        sys_info = SystemInfo()
        uptime_info = sys_info.get_uptime_info()
        if json_output:
            print_json(uptime_info)
        else:
            print_formatted("System Uptime", uptime_info)

    def show_users(self, json_output, verbose):
        sys_info = SystemInfo()
        user_info = sys_info.get_user_info(verbose)
        if json_output:
            print_json(user_info)
        else:
            for user in user_info:
                print_formatted(f"Username: {user['Username']}", user)

    def show_version(self, json_output):
        from .__init__ import __version__
        version_info = {"OSPeek CLI": f"v{__version__}"}
        if json_output:
            print_json(version_info)
        else:
            print_formatted("Version", version_info)

    def show_help(self):
        self.parser.print_help()