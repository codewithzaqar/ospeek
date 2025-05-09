# OSPeek
A simple CLI tool to display system information

## Installation
```bash
pip install .
```
## Usage
```bash
ospeek info [--json] [--verbose]                                                                               # Show system, CPU, and memory info
ospeek disk [--json]                                                                                           # Show disk usage info
ospeek network [--json]                                                                                        # Show network interface info
ospeek processes [--json] [--verbose] [--sort {cpu,memory,pid}] [--refresh <seconds>] [--filter <name_or_pid>] # Show running processes info
ospeek uptime [--json]                                                                                         # Show system uptime and boot time
ospeek users [--json] [--verbose] [--refresh <seconds>]                                                        # Show logged-in users info
ospeek battery [--json]                                                                                        # Show battery status and capacity
ospeek temperature [--json]                                                                                    # Show temperature sensor data
ospeek fan [--json]                                                                                            # Show fan speed data
ospeek version [--json]                                                                                        # Show CLI version
ospeek help                                                                                                    # Show help
```