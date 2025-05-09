import argparse
from .system_info import SystemInfo
from .utils import print_formatted

class OSPeekCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="OSPeek CLI v0.0.2")
        self.parser.add_argument(
            "command",
            choices=["info", "disk", "network", "version", "help"],
            help="Command to execute",
            nargs="?",
            default="help",
        )

    def run(self, args):
        args = self.parser.parse_args(args)
        if args.command == "info":
            self.show_info()
        elif args.command == "disk":
            self.show_disk()
        elif args.command == "network":
            self.show_network()
        elif args.command == "version":
            self.show_version()
        else:
            self.show_help()

    def show_info(self):
        sys_info = SystemInfo()
        info = sys_info.get_system_info()
        print_formatted("System Information", info["system"])
        print_formatted("CPU Information", info["cpu"])
        print_formatted("Memory Information", info["memory"])

    def show_disk(self):
        sys_info = SystemInfo()
        disk_info = sys_info.get_disk_info()
        print_formatted("Disk Usage", disk_info)

    def show_network(self):
        sys_info = SystemInfo()
        network_info = sys_info.get_network_info()
        for interface in network_info:
            print_formatted(f"Interface: {interface['Interface']}", interface)

    def show_version(self):
        from .__init__ import __version__
        print_formatted("Version", {"OSPeek CLI": f"v{__version__}"})

    def show_help(self):
        self.parser.print_help()