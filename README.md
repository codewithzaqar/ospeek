<img align="center" src="images/OSPeek_logo.png" width=250>

# OSPeek
A simple CLI tool to display system information

## Installation
```bash
pip install .
```
## Usage
```bash
ospeek info [--json] [--verbose]                                                                                                   # Show system, CPU, and memory info
ospeek disk [--json]                                                                                                               # Show disk usage info
ospeek network [--json]                                                                                                            # Show network interface info
ospeek processes [--json] [--verbose] [--sort {cpu,memory,pid}] [--refresh <seconds>] [--filter <name_or_pid>]                     # Show running processes info
ospeek uptime [--json]                                                                                                             # Show system uptime and boot time
ospeek users [--json] [--verbose] [--refresh <seconds>]                                                                            # Show logged-in users info
ospeek battery [--json]                                                                                                            # Show battery status and capacity
ospeek temperature [--json] [--watch <seconds>]                                                                                    # Show temperature sensor data
ospeek fan [--json] [--watch <seconds>]                                                                                            # Show fan speed data
ospeek services [--json] [--count <number>]                                                                                        # Show system service info
ospeek logs [--json] [--count <number>]                                                                                            # Show recent system log entries
ospeek version [--json]                                                                                                            # Show CLI version
ospeek help                                                                                                                        # Show help
```