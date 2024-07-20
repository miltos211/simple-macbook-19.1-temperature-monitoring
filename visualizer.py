import os
import urllib.request
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import sys

# Configuration
USE_CUSTOM_IMAGE = False  # Set to True to override the default image
CUSTOM_IMAGE_URL = 'https://example.com/custom_image.png'  # Replace with your custom image URL
CUSTOM_IMAGE_PATH = 'assets/custom_image.png'  # Replace with your custom image path if already downloaded

# Terminal logging function
def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

log("Starting the temperature visualization script...")

try:
    # Ensure assets folder and image are present
    assets_dir = 'assets'
    default_image_name = 'apple-macbook-pro-2019-16-1660572442-1795526580.png'
    image_path = CUSTOM_IMAGE_PATH if USE_CUSTOM_IMAGE else os.path.join(assets_dir, default_image_name)
    
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        log(f"Created assets directory: {assets_dir}")

    if not os.path.exists(image_path):
        image_url = CUSTOM_IMAGE_URL if USE_CUSTOM_IMAGE else 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ffiles.refurbed.com%2Fii%2Fapple-macbook-pro-2019-16-1660572442.jpg&f=1&nofb=1&ipt=4d10147736efcc9eb83a9de8d76549289311cdfa4e582bc357d74d0327c8d87f&ipo=images'
        urllib.request.urlretrieve(image_url, image_path)
        log(f"Downloaded image to: {image_path}")

    # Define the log directory
    log_dir = 'logs_for_visualizer_test'
    csv_file_path = os.path.join(log_dir, 'system_metrics.csv')

    log(f"Checking if CSV file exists at path: {csv_file_path}")

    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    log(f"CSV file found at path: {csv_file_path}")

    # Load and process the CSV data
    data = pd.read_csv(csv_file_path)
    log(f"Loaded data from CSV file: {csv_file_path}")

    # Check the data contents for debugging
    log(f"CSV data head: \n{data.head()}")

    # Define positions for the temperature labels using your coordinates
    positions = {
        'fan 1 (left)': (430, 736),
        'fan 2 (right)': (1158, 738),
        'cpu': (608, 709),
        'gpu': (878, 704),
        'battery location 1': (720, 952),
        'battery location 2': (361, 1086),
        'battery location 3': (1131, 1099),
        'palmrest middle': (759, 1143),
    }

    # Function to draw a rectangle with gradient color based on temperature
    def draw_gradient_rectangle(draw_obj, top_left, bottom_right, color):
        for y in range(top_left[1], bottom_right[1]):
            for x in range(top_left[0], bottom_right[0]):
                draw_obj.point((x, y), fill=color)

    # Update sensor map to easily add or change sensor locations
    sensor_map = {
        'fan 1 (left)': '_Fan_Stats_ Temperature (°C)',
        'fan 2 (right)': '_Fan_Stats_ Temperature (°C)',
        'cpu': '_CPU_Stats_ Temperature (°C)',
        'gpu': '_Extra_Stats_ Temperature (°C)',
        'battery location 1': '_Battery_Stats_ Temperature (°C)',
        'battery location 2': '_Battery_Stats_ Temperature (°C)',
        'battery location 3': '_Battery_Stats_ Temperature (°C)',
        'palmrest middle': '_Extra_Stats_ Temperature (°C)',
    }

    # Get all unique timestamps from the data
    unique_timestamps = pd.to_datetime(data['Timestamp']).unique()

    # Initialize a variable to track if the first image has been shown
    first_image_shown = False

    # Create a directory for the current run's date-time
    current_run_dir = os.path.join(assets_dir, datetime.now().strftime('%Y%m%d_%H%M%S'))
    os.makedirs(current_run_dir, exist_ok=True)
    log(f"Created directory for current run: {current_run_dir}")

    # Process each timestamp separately
    for timestamp in unique_timestamps:
        # Filter data for the current timestamp's 30-second window
        time_threshold = timestamp - timedelta(seconds=30)
        filtered_data = data[(pd.to_datetime(data['Timestamp']) >= time_threshold) & (pd.to_datetime(data['Timestamp']) <= timestamp)]

        if filtered_data.empty:
            log(f"No data found for the 30-second window ending at {timestamp}")
            continue

        # Calculate average temperatures over the 30-second window
        temperature_columns = [col for col in data.columns if 'Temperature' in col]
        average_temperatures = filtered_data[temperature_columns].mean()
        log(f"Calculated average temperatures for the 30-second window ending at {timestamp}")

        # Load the image and convert to black and white
        image = Image.open(image_path).convert("L").convert("RGBA")
        log("Loaded and converted MacBook image to black and white.")

        # Define the color map
        cmap = plt.get_cmap('coolwarm')  # Blue to red color map

        # Normalize the temperature data for color mapping
        norm = plt.Normalize(vmin=average_temperatures.min(), vmax=average_temperatures.max())

        # Create an overlay image for temperatures and labels
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        font = ImageFont.load_default()

        # Create a mask for the temperature overlay
        temp_overlay = Image.new('RGBA', image.size)
        temp_draw = ImageDraw.Draw(temp_overlay)

        # Paint the entire image with colors corresponding to the temperature values
        for label, csv_col in sensor_map.items():
            if csv_col in average_temperatures and label in positions:
                temp = average_temperatures[csv_col]
                color = tuple(int(c * 255) for c in cmap(norm(temp))[:3]) + (165,)  # Add opacity
                position = positions[label]
                rect_size = (150, 150)  # Size of the rectangle for each sensor
                top_left = (position[0] - rect_size[0] // 2, position[1] - rect_size[1] // 2)
                bottom_right = (position[0] + rect_size[0] // 2, position[1] + rect_size[1] // 2)
                draw_gradient_rectangle(temp_draw, top_left, bottom_right, color)
                log(f"Painted {label} area with temperature {temp:.2f}°C")

        # Blend temperature values in overlapping areas
        blended = Image.alpha_composite(image, temp_overlay)

        # Draw the labels on the overlay with a dark background
        for label, csv_col in sensor_map.items():
            if csv_col in average_temperatures and label in positions:
                temp = average_temperatures[csv_col]
                position = positions[label]
                text = f"{label}: {temp:.2f}°C"
                text_size = draw.textbbox((0, 0), text, font=font)[2:]  # Get the size of the text
                label_bg = Image.new('RGBA', text_size, (0, 0, 0, 100))
                blended.paste(label_bg, position, label_bg)
                draw = ImageDraw.Draw(blended)
                draw.text(position, text, fill=(255, 255, 255, 255), font=font)
                log(f"Added label for {label} with temperature {temp:.2f}°C at position {position}")

        # Add the timestamp
        draw.text((10, 10), f"Avg Temp over last 30s up to {timestamp.strftime('%Y-%m-%d %H:%M:%S')}", fill=(255, 255, 255, 255), font=font)
        log("Added timestamp to image.")

        # Save the result as PNG
        output_image_path = os.path.join(current_run_dir, f"temperature_visual_{timestamp.strftime('%H%M%S')}.png")
        blended.save(output_image_path)
        log(f"Image saved to: {output_image_path}")

        # Show the first and last image only
        if not first_image_shown:
            blended.show()
            first_image_shown = True

    # Show the last image
    blended.show()

except Exception as e:
    log(f"Error: {e}")
    sys.exit(1)

log("Temperature visualization script completed.")
