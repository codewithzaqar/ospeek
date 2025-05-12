import json
import os
import platform

try:
    from plyer import notification
except ImportError:
    notification = None

def print_formatted(title, data):
    print(f"\n{title}:")
    print("-" * 50)
    for key, value in data.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    print("-" * 50)

def print_process_table(title, processes, verbose=False):
    print(f"\n{title}:")
    print("-" * 50)
    if processes and "Status" in processes[0]:
        print(f"{processes[0]['Status']}")
    else:
        if verbose:
            header = f"{'PID':<10} {'Name':<20} {'CPU (%)':<10} {'Memory (MB)':<12} {'Status':<10} {'User':<15}"
        else:
            header = f"{'PID':<10} {'Name':<20} {'CPU (%)':<10} {'Memory (MB)':<12}"
        print(header)
        print("-" * 50)
        for proc in processes:
            if verbose:
                print(f"{proc['PID']:<10} {proc['Name'][:19]:<20} {proc['CPU (%)']:<10.2f} {proc['Memory (MB)']:<12.2f} {proc['Status']:<10} {proc['User'][:14]:<15}")
            else:
                print(f"{proc['PID']:<10} {proc['Name'][:19]:<20} {proc['CPU (%)']:<10.2f} {proc['Memory (MB)']:<12.2f}")
    print("-" * 50)

def print_json(data):
    print(json.dumps(data, indent=2))

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def send_notification(title, message):
    if notification:
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="OSPeek",
                timeout=10
            )
            print(f"[Desktop notification: \"{title}: {message}\"]")
        except Exception as e:
            print(f"[Failed to send notification: {str(e)}]")
    else:
        print("[Notifications unavailable: player not installed]")