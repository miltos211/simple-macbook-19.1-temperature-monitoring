import os
from PIL import Image, ImageSequence
import sys
from datetime import datetime

# Terminal logging function
def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

log("Starting the GIF creation script...")

try:
    # Ensure assets directory is present
    assets_dir = 'assets'
    if not os.path.exists(assets_dir):
        raise FileNotFoundError(f"Assets directory not found: {assets_dir}")

    # List available directories
    directories = [d for d in os.listdir(assets_dir) if os.path.isdir(os.path.join(assets_dir, d))]
    if not directories:
        raise FileNotFoundError(f"No directories found in assets: {assets_dir}")

    # Display available directories to the user
    print("Available directories:")
    for idx, directory in enumerate(directories, start=1):
        print(f"{idx}. {directory}")

    # Prompt user to select a directory
    selected_idx = int(input("Select a directory by number: ")) - 1
    if selected_idx < 0 or selected_idx >= len(directories):
        raise ValueError("Invalid selection")

    selected_dir = directories[selected_idx]
    selected_dir_path = os.path.join(assets_dir, selected_dir)
    log(f"Selected directory: {selected_dir_path}")

    # Get list of images in the selected directory
    images = [img for img in os.listdir(selected_dir_path) if img.endswith('.png')]
    if not images:
        raise FileNotFoundError(f"No PNG images found in directory: {selected_dir_path}")

    images.sort()  # Ensure images are in order
    log(f"Found {len(images)} images in directory: {selected_dir_path}")

    # Load images
    frames = [Image.open(os.path.join(selected_dir_path, img)) for img in images]

    # Convert images to have the same mode and size
    first_frame = frames[0]
    converted_frames = [frame.convert("RGBA").resize(first_frame.size) for frame in frames]

    # Create the GIF
    output_gif_path = os.path.join(selected_dir_path, f"temperature_graph_{selected_dir}.gif")
    converted_frames[0].save(output_gif_path, save_all=True, append_images=converted_frames[1:], duration=5000, loop=0)
    log(f"GIF saved to: {output_gif_path}")

    # Optionally show the first and last frames for visualization
    converted_frames[0].show()
    converted_frames[-1].show()

except Exception as e:
    log(f"Error: {e}")
    sys.exit(1)

log("GIF creation script completed.")
