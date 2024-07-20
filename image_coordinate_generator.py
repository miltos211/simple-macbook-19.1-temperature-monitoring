import os
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk

# Create a directory for logs
log_dir = "clicker_log"
os.makedirs(log_dir, exist_ok=True)

# Function to log the click coordinates and label
def log_click(event):
    x, y = event.x, event.y
    label = simpledialog.askstring("Input", f"Enter a label for coordinates ({x}, {y}):")
    if label:
        with open(os.path.join(log_dir, "click_log.txt"), "a") as log_file:
            log_file.write(f"Coordinates: ({x}, {y}), Label: {label}\n")

# Function to display the image and set up the click event
def display_image(image_path):
    root = tk.Tk()
    root.title("Click Logger")

    # Open the image file
    img = Image.open(image_path)
    img_tk = ImageTk.PhotoImage(img)

    # Create a label to display the image
    label = tk.Label(root, image=img_tk)
    label.image = img_tk  # Keep a reference to avoid garbage collection
    label.pack()

    # Bind the click event to the log_click function
    label.bind("<Button-1>", log_click)

    root.mainloop()

# Path to your PNG file
image_path = "assets/apple-macbook-pro-2019-16-1660572442-1795526580.png"

# Run the display_image function
display_image(image_path)
