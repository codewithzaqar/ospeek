# OSPeek
A simple CLI tool to display system information

## Installation
```bash
pip install .
```
## Usage
```bash
ospeek info [--json] [--verbose]      # Show system, CPU, and memory info
ospeek disk [--json]                  # Show disk usage info
ospeek network [--json]               # Show network interface info
ospeek processes [--json] [--verbose] # Show running processes info
ospeek uptime [--json]                # Show system uptime and boot time
ospeek users [--json] [--verbose]     # Show logged-in users info
ospeek version [--json]               # Show CLI version
ospeek help                           # Show help
```