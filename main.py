import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk

# Function to generate QR code
def generate_qr_code(input_text):
    if not input_text.strip():
        messagebox.showerror("Error", "Input cannot be empty!")
        return None

    # Generate the QR code with larger size
    qr = qrcode.QRCode(version=1, box_size=20, border=2)  # Increased box_size for larger QR code
    qr.add_data(input_text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Function to display QR code in the app
def display_qr_code(image):
    global qr_image_tk  # Keep a reference to avoid garbage collection
    img_width, img_height = image.size
    if img_width > 300 or img_height > 300:  # Resize image if needed
        image = image.resize((300, 300), Image.Resampling.LANCZOS)  # Updated resizing method
    qr_image_tk = ImageTk.PhotoImage(image)
    qr_code_label.config(image=qr_image_tk)
    qr_code_label.image = qr_image_tk

# Function to save QR code as an image
def save_qr_code(image):
    if image is None:
        messagebox.showerror("Error", "No QR code to save!")
        return

    filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png")])
    if filepath:
        image.save(filepath)
        messagebox.showinfo("Success", f"QR code saved as {filepath}")

# Function triggered by "Generate QR Code" button
def on_generate_click():
    input_text = input_field.get()
    qr_image = generate_qr_code(input_text)
    if qr_image:
        display_qr_code(qr_image)
        global current_qr_image
        current_qr_image = qr_image

# Function triggered by "Save as Image" button
def on_save_click():
    save_qr_code(current_qr_image)

# Function to quit the application
def quit_app():
    root.destroy()

# Initialize main Tkinter window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x600")
root.resizable(False, False)

# Input field for text/URL
input_label = tk.Label(root, text="Enter text or URL:", font=("Arial", 14))
input_label.pack(pady=10)

input_field = tk.Entry(root, font=("Arial", 14), width=30)
input_field.pack(pady=10)

# Buttons: Generate, Save, and Quit
generate_button = tk.Button(root, text="Generate QR Code", font=("Arial", 14), command=on_generate_click)
generate_button.pack(pady=10)

save_button = tk.Button(root, text="Save as Image", font=("Arial", 14), command=on_save_click)
save_button.pack(pady=10)

quit_button = tk.Button(root, text="Quit", font=("Arial", 14), command=quit_app)
quit_button.pack(pady=10)

# Area to display QR code
qr_code_label = tk.Label(root, text="Your QR Code will appear here", font=("Arial", 12), bg="gray", width=300, height=300)
qr_code_label.pack(pady=20)

# Variable to store the current QR code image
current_qr_image = None

# Start Tkinter event loop
root.mainloop()
