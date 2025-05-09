import json

def print_formatted(title, data):
    print(f"\n{title}:")
    print("-" * 50)
    for key, value in data.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    print("-" * 50)

def print_process_table(title, processes):
    print(f"\n{title}:")
    print("-" * 50)
    header = f"{'PID':<10} {'Name':<20} {'CPU (%)':<10} {'Memory (MB)':<12}"
    print(header)
    print("-" * 50)
    for proc in processes:
        print(f"{proc['PID']:<10} {proc['Name'][:19]:<20} {proc['CPU (%)']:<10.2f} {proc['Memory (MB)']:<12.2f}")
    print("-" * 50)

def print_json(data):
    print(json.dumps(data, indent=2))