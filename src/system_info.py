import platform

class SystemInfo:
    def get_system_info(self):
        return {
            "OS": platform.system(),
            "OS Version": platform.release(),
            "Architecture": platform.machine(),
            "Node Name": platform.node(),
        }