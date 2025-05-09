import json
import os
import platform

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