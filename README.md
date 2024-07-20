# simple-macbook-19.1-temperature-monitoring

## Author's Note

I bought a MacBook to run games, bad idea right? I've noticed a few issues with running games, especially in the temperature department. So I created this project to help me understand where I can improve temperature-wise (e.g., do a thermal pad mod on the VRMs and measure how good it is, or change the charger location from the left-hand side of the laptop to the right, and so on).

## Features

- Monitors CPU usage, memory usage, and CPU temperature.
- Detects "heavy applications" based on CPU and memory usage.
- Logs system metrics to a CSV file.
- Can run in debug mode to provide detailed logging output to the terminal.
- Visualizes temperature data on a MacBook image.
- Creates an animated GIF from the visualized images.

## Requirements

- Python 3.6 or higher
- iStats (for reading temperature sensors)
- Tkinter (for running the clicker script)

## Installation

### Python Dependencies

Install the required Python packages using pip:

```sh
pip install -r requirements.txt
```

### iStats Installation

The script checks if `iStats` is installed and functional. If not, it attempts to install it using:

```sh
sudo gem install iStats
```

Ensure you have Ruby and the `gem` command installed on your system. You can install Ruby using Homebrew if it's not already installed:

```sh
brew install ruby
```

### Tkinter Installation

Tkinter can be installed via Homebrew:

```sh
brew install python-tk
```

## Setup Instructions

### Cloning the Repository

```sh
git clone https://github.com/yourusername/simple-macbook-19.1-temperature-monitoring.git
cd simple-macbook-19.1-temperature-monitoring
```

### Virtual Environment Setup

Create and activate a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Then install the dependencies:

```sh
pip install -r requirements.txt
```

## Usage

### Monitor Script

Run the script with the following command:

```sh
python monitor.py
```

To enable debug mode, which provides detailed logging output to the terminal, use the `-d` or `--debug` flag:

```sh
python monitor.py -d
```

### Visualizer Script

Run the visualizer script to create images with temperature data:

```sh
python visualizer.py
```

### Gififier Script

Run the gififier script to create an animated GIF from the visualized images:

```sh
python gififier.py
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

### Visualization

The visualizer script uses the collected data to overlay temperature readings on an image of a MacBook. The positions of the sensors are hardcoded based on coordinates obtained using a clicker script.

### Clicker Script

To determine the positions of the sensors on the MacBook image, a clicker script is used. The clicker script allows you to click on the image and records the coordinates in a file named `click_log.txt` in the `clicker_log` directory.

### Gififier Script

The gififier script stitches all images together into an animated GIF, with each image shown for 5 seconds.

## Project Structure

```
simple-macbook-19.1-temperature-monitoring/
│
├── assets/
│   └── apple-macbook-pro-2019-16-1660572442-1795526580.png   # MacBook image for visualization
│   └── {timestamped directories}/                            # Directories for output images
│
├── logs/
│   └── system_metrics.log        # Log file for system metrics
│   └── system_metrics.csv        # CSV file for system metrics
│
├── logs_for_visualizer_test/
│   └── system_metrics.log        # Log file for test metrics
│   └── system_metrics.csv        # CSV file for test metrics
│
├── clicker_log/
│   └── click_log.txt             # Log file for clicker coordinates
│
├── monitor.py                    # Main script for monitoring
├── visualizer.py                 # Script for visualizing temperature data
├── gififier.py                   # Script for creating an animated GIF
├── requirements.txt              # List of Python dependencies
└── start.sh                      # Shell script for starting the monitoring
```

## Example Output

### Terminal Output (Debug Mode)

```sh
2024-07-20 22:17:09,840 TERM_PROGRAM=Apple_Terminal
2024-07-20 22:17:09,841 SHELL=/bin/zsh
...
2024-07-20 22:22:27,125 Command 'istats --version' failed with error: iStats v1.6.2
2024-07-20 22:22:27,126 iStats not found. Installing iStats...
Timestamp: 2024-07-20 22:17:09, CPU Usage (%): 12.3, Memory Usage (%): 53.7, CPU Temperature (°C): 40.5
```

### CSV Output

```csv
Timestamp,CPU Usage (%),Memory Usage (%),_CPU_Stats_ Temperature (°C),_Fan_Stats_ Temperature (°C),_Battery_Stats_ Temperature (°C),_Extra_Stats_ Temperature (°C)
2024-07-20 22:17:09,12.3,53.7,40.5,2.0,91.0,37.44
2024-07-20 22:17:19,11.7,54.1,41.2,2.0,91.0,37.44
...
```

### Visualizer Output

Images are saved in the `assets/{timestamped directories}/` directory, displaying the average temperatures over the last 30 seconds on a MacBook image.

### Gififier Output

An animated GIF is created from the visualized images, with each image shown for 5 seconds. The GIF is saved in the `assets/` directory with a filename based on the current date and time.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.

## Additional Information

Make sure to update the `click_log.txt` file with the correct coordinates for your sensors using the clicker script to ensure accurate visualization.

## Future Work and Improvements

- Adding support for different MacBooks and Macs in general.
- Adding Touch Bar support.
- Implementing notifications for critical temperatures.

## Acknowledgments

- Thanks to the creators of `iStats` for providing a simple way to access sensor data on macOS.
- Thanks to the Python community for the amazing libraries and tools that make projects like this possible.
