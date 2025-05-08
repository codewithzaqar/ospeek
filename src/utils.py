def print_formatted(title, data):
    print(f"\n{title}:")
    print("-" * 50)
    for key, value in data.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    print("-" * 50)