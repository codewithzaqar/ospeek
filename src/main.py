import sys
from .cli import OSPeekCLI

def main():
    cli = OSPeekCLI()
    cli.run(sys.argv[1:])

if __name__ == "__main__":
    main()