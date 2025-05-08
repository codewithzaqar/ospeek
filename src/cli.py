import argparse
from .system_info import SystemInfo
from .utils import print_formatted

class OSPeekCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="OSPeek CLI v0.0.1")
        self.parser.add_argument(
            "command",
            choices=["info", "version", "help"],
            help="Command to execute",
            nargs="?",
            default="help",
        )

    def run(self, args):
        args = self.parser.parse_args(args)
        if args.command == "info":
            self.show_info()
        elif args.command == "version":
            self.show_version()
        else:
            self.show_help()

    def show_info(self):
        sys_info = SystemInfo()
        info = sys_info.get_system_info()
        print_formatted("System Information", info)

    def show_version(self):
        from .__init__ import __version__
        print_formatted("Version", {"OSPeek CLI": f"v{__version__}"})

    def show_help(self):
        self.parser.print_help()