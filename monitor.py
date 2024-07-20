import psutil
import time
import logging
import subprocess
import pandas as pd
from datetime import datetime
import os
import argparse
import re

# Parse command-line arguments
parser = argparse.ArgumentParser(description='System Monitoring Script')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging to terminal')
args = parser.parse_args()

# Create logs directory if it doesn't exist
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Initialize logging
log_file = os.path.join(log_dir, 'system_metrics.log')
logging.basicConfig(filename=log_file, level=logging.DEBUG if args.debug else logging.INFO, format='%(asctime)s %(message)s')

if args.debug:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logging.getLogger().addHandler(console_handler)

# Function to ensure iStats is installed
def ensure_istats_installed():
    try:
        subprocess.check_output(["istats", "--version"])
        logging.info("iStats is already installed.")
    except FileNotFoundError:
        logging.info("iStats not found. Installing iStats...")
        try:
            subprocess.check_call(["sudo", "gem", "install", "iStats"])
            logging.info("iStats installed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error installing iStats: {e}")
    except Exception as e:
        logging.error(f"Error checking iStats: {e}")

# Function to ensure all sensors are enabled
def ensure_sensors_enabled():
    try:
        # Check if any sensors are enabled
        temp_output = subprocess.check_output(["istats", "all", "--value-only"]).decode('utf-8')
        if not temp_output.strip():
            logging.info("No sensors found, enabling all sensors.")
            enable_all_sensors()
        else:
            logging.info("Sensors are already enabled.")
    except FileNotFoundError:
        logging.warning("istats utility not found.")
    except Exception as e:
        logging.error(f"Error checking sensors: {e}")

# Function to enable all sensors
def enable_all_sensors():
    try:
        # Scan for available sensors
        scan_output = subprocess.check_output(["istats", "scan"]).decode('utf-8')
        logging.debug(f"istats scan output:\n{scan_output}")
        
        # Enable all sensors
        enable_output = subprocess.check_output(["istats", "enable", "all"]).decode('utf-8')
        logging.debug(f"istats enable all output:\n{enable_output}")
    except FileNotFoundError:
        logging.warning("istats utility not found. Install it using 'sudo gem install iStats'.")
    except Exception as e:
        logging.error(f"Error enabling sensors: {e}")

# Function to get system metrics
def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    temperature_sensors = get_temperature_sensors()
    
    metrics = {
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'CPU Usage (%)': cpu_usage,
        'Memory Usage (%)': memory_info.percent,
    }
    metrics.update(temperature_sensors)
    return metrics

# Function to get temperature sensors using istats
def get_temperature_sensors():
    try:
        temp_output = subprocess.check_output(["istats", "all", "--value-only"]).decode('utf-8')
        logging.debug(f"istats output:\n{temp_output}")
        
        # Extract temperature readings
        sensor_lines = temp_output.strip().split('\n')
        sensors = {}
        current_sensor = None
        for line in sensor_lines:
            if "---" in line:
                current_sensor = line.strip().replace('---', '').replace(' ', '_')
                continue
            try:
                temp_value = float(line.strip())
                if current_sensor:
                    sensors[f'{current_sensor} Temperature (°C)'] = temp_value
                    current_sensor = None
            except ValueError:
                logging.error(f"Error converting temperature value: {line.strip()}")
            logging.debug(f"Skipping line: {line}")
        logging.debug(f"Temperature sensors: {sensors}")
        return sensors
    except FileNotFoundError:
        logging.warning("istats utility not found. Install it using 'sudo gem install iStats'.")
        return {}
    except Exception as e:
        logging.error(f"Error getting temperature sensors: {e}")
        return {}

# Function to log metrics to CSV
def log_metrics_to_csv(metrics, filename='system_metrics.csv'):
    df = pd.DataFrame([metrics])
    csv_file = os.path.join(log_dir, filename)
    try:
        df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)
    except FileNotFoundError:
        df.to_csv(csv_file, mode='a', header=True, index=False)

# Function to detect heavy applications
def detect_heavy_application():
    heavy_app_threshold = {'cpu': 50, 'memory': 1 * 1024 * 1024 * 1024}  # 50% CPU, 1GB RAM
    heavy_apps = []
    
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            cpu_usage = process.info['cpu_percent']
            memory_info = process.info['memory_info']
            if memory_info is not None:
                memory_usage = memory_info.rss  # Resident Set Size
                if cpu_usage > heavy_app_threshold['cpu'] and memory_usage > heavy_app_threshold['memory']:
                    heavy_apps.append((process.info['name'], cpu_usage, memory_usage))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    return heavy_apps

# Main function
if __name__ == "__main__":
    heavy_app_running = {}

    # Ensure iStats is installed
    ensure_istats_installed()

    # Ensure sensors are enabled
    ensure_sensors_enabled()
    
    while True:
        metrics = get_system_metrics()
        log_metrics_to_csv(metrics)
        
        # Format the metrics for logging and printing
        formatted_metrics = ", ".join([f"{key}: {value}" for key, value in metrics.items()])
        logging.info(formatted_metrics)
        print(formatted_metrics)
        
        heavy_apps = detect_heavy_application()
        current_time = datetime.now()
        
        for app, cpu, memory in heavy_apps:
            if app not in heavy_app_running:
                heavy_app_running[app] = {'start_time': current_time, 'cpu': cpu, 'memory': memory}
                logging.info(f"Potential heavy application detected: {app} (CPU: {cpu}%, Memory: {memory} bytes)")
            elif (current_time - heavy_app_running[app]['start_time']).seconds > 60:
                logging.info(f"Heavy application confirmed: {app} (CPU: {cpu}%, Memory: {memory} bytes)")
        
        # Clean up apps that no longer meet the criteria
        for app in list(heavy_app_running.keys()):
            if app not in [ha[0] for ha in heavy_apps]:
                del heavy_app_running[app]
        
        time.sleep(10)  # Adjust interval as needed
