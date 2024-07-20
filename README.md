# simple-macbook-19.1-temperature-monitoring

A very simple Python-based temperature monitoring system with a detection mechanism for "heavy apps". This script helps monitor the CPU temperature, memory usage, and CPU usage on a MacBook, and it detects applications that are using a significant amount of resources.

## Features

- Monitors CPU usage, memory usage, and CPU temperature.
- Detects "heavy applications" based on CPU and memory usage.
- Logs system metrics to a CSV file.
- Can run in debug mode to provide detailed logging output to the terminal.

## Requirements

- Python 3.6 or higher
- iStats (for reading temperature sensors)

## Installation

### Python Dependencies

Install the required Python packages using pip:

```
pip install -r requirements.txt
```

### iStats Installation

The script checks if `iStats` is installed and functional. If not, it attempts to install it using:

```
sudo gem install iStats
```

Ensure you have Ruby and the `gem` command installed on your system. You can install Ruby using Homebrew if it's not already installed:

```
brew install ruby
```

## Usage

Run the script with the following command:

```
python monitor.py
```

To enable debug mode, which provides detailed logging output to the terminal, use the `-d` or `--debug` flag:

```
python monitor.py -d
```

## Script Overview

### Environment Setup

The script ensures `iStats` is installed and all temperature sensors are enabled. It sources the appropriate shell configuration (`.zshrc` or `.bashrc`) based on the current shell.

### Metrics Collection

The script collects the following metrics:
- CPU usage
- Memory usage
- CPU temperature and other available temperature sensors

### Heavy Application Detection

A "heavy application" is defined as one that uses more than 50% CPU and 1GB of memory for over a minute.

### Logging and Output

The collected metrics are logged in a CSV file located in the `logs` directory. Additionally, metrics and detected heavy applications are printed to the terminal.
Check logs_for_visualiser_test for example logs.

## Project Structure

```
simple-macbook-19.1-temperature-monitoring/
│
├── logs/
│   └── system_metrics.log        # Log file for system metrics
│   └── system_metrics.csv        # CSV file for system metrics
│
├── monitor.py                    # Main script for monitoring
└── requirements.txt              # List of Python dependencies
```

## Example Output

### Terminal Output (Debug Mode)

```
2024-07-20 22:17:09,840 TERM_PROGRAM=Apple_Terminal
2024-07-20 22:17:09,841 SHELL=/bin/zsh
...
2024-07-20 22:22:27,125 Command 'istats --version' failed with error: iStats v1.6.2
2024-07-20 22:22:27,126 iStats not found. Installing iStats...
Timestamp: 2024-07-20 22:17:09, CPU Usage (%): 12.3, Memory Usage (%): 53.7, CPU Temperature (°C): 40.5
```

### CSV Output

```
Timestamp,CPU Usage (%),Memory Usage (%),CPU Temperature (°C)
2024-07-20 22:17:09,12.3,53.7,40.5
2024-07-20 22:17:19,11.7,54.1,41.2
...
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.
