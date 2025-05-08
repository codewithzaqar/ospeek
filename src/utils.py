def print_formatted(title, data):
    print(f"\n{title}:")
    print("-" * 50)
    for key, value in data.items():
        print(f"{key}: {value}")
    print("-" * 50)