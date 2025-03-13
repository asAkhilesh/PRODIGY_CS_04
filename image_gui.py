import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button, Frame
from tkinterdnd2 import DND_FILES, TkinterDnD
from cryptography.fernet import Fernet
from PIL import Image, ImageTk
import os

# Generate key if not exists
def generate_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        print("Encryption key generated successfully!")

# Load encryption key
def load_key():
    return open("secret.key", "rb").read()

# Function to show selected image
def show_image(file_path):
    img = Image.open(file_path)
    img = img.resize((200, 200))  # Resize for preview
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img  # Keep a reference

# Function to handle file drop
def on_drop(event):
    file_path = event.data.strip("{}")  # Remove curly brackets if dragged from explorer
    selected_file.set(file_path)
    show_image(file_path)

# Encrypt Image
def encrypt_image():
    file_path = selected_file.get()
    if not file_path:
        messagebox.showerror("Error", "No image selected!")
        return

    key = load_key()
    img = cv2.imread(file_path)
    img_data = np.array(img)

    # Flatten and XOR encrypt
    flat_img = img_data.flatten()
    encrypted_data = bytearray([b ^ key[i % len(key)] for i, b in enumerate(flat_img)])
    
    encrypted_img = np.array(encrypted_data).reshape(img_data.shape)
    encrypted_path = file_path.replace(".", "_encrypted.")
    cv2.imwrite(encrypted_path, encrypted_img)

    messagebox.showinfo("Success", f"Image Encrypted! Saved as {encrypted_path}")

# Decrypt Image
def decrypt_image():
    file_path = selected_file.get()
    if not file_path:
        messagebox.showerror("Error", "No image selected!")
        return

    key = load_key()
    img = cv2.imread(file_path)
    img_data = np.array(img)

    # Flatten and XOR decrypt
    flat_img = img_data.flatten()
    decrypted_data = bytearray([b ^ key[i % len(key)] for i, b in enumerate(flat_img)])
    
    decrypted_img = np.array(decrypted_data).reshape(img_data.shape)
    decrypted_path = file_path.replace("_encrypted", "_decrypted")
    cv2.imwrite(decrypted_path, decrypted_img)

    messagebox.showinfo("Success", f"Image Decrypted! Saved as {decrypted_path}")

# Function to select file manually
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        selected_file.set(file_path)
        show_image(file_path)

# Function to clear selected image
def clear_image():
    selected_file.set("")
    image_label.config(image="")
    image_label.image = None

# Button hover effects
def on_hover(widget, color):
    widget.config(bg=color)

def off_hover(widget, color):
    widget.config(bg=color)

# GUI Setup
generate_key()  # Ensure key exists before running GUI
root = TkinterDnD.Tk()
root.title("🔒 Advanced Image Encryption Tool")
root.geometry("500x550")
root.configure(bg="#222831")

# Drag & Drop Frame
drop_frame = Frame(root, bg="#393E46", width=450, height=80)
drop_frame.pack(pady=10)
drop_label = Label(drop_frame, text="Drag & Drop an Image Here", fg="white", bg="#393E46", font=("Arial", 12, "bold"))
drop_label.pack(pady=20)

# Enable drag & drop
root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", on_drop)

# Selected File
selected_file = tk.StringVar()

# Image Preview
image_label = Label(root, bg="#222831")
image_label.pack(pady=10)

# Buttons with hover effects
button_style = {
    "font": ("Arial", 12, "bold"),
    "padx": 20,
    "pady": 10,
    "width": 20,
    "relief": "raised",
    "bd": 3
}

encrypt_btn = Button(root, text="🔐 Encrypt Image", command=encrypt_image, fg="white", bg="#00ADB5", **button_style)
encrypt_btn.pack(pady=10)
encrypt_btn.bind("<Enter>", lambda e: on_hover(encrypt_btn, "#008C8C"))
encrypt_btn.bind("<Leave>", lambda e: off_hover(encrypt_btn, "#00ADB5"))

decrypt_btn = Button(root, text="🔓 Decrypt Image", command=decrypt_image, fg="white", bg="#FF5722", **button_style)
decrypt_btn.pack(pady=10)
decrypt_btn.bind("<Enter>", lambda e: on_hover(decrypt_btn, "#D84315"))
decrypt_btn.bind("<Leave>", lambda e: off_hover(decrypt_btn, "#FF5722"))

select_btn = Button(root, text="📁 Select Image Manually", command=select_file, fg="black", bg="lightgray", **button_style)
select_btn.pack(pady=10)
select_btn.bind("<Enter>", lambda e: on_hover(select_btn, "#B0BEC5"))
select_btn.bind("<Leave>", lambda e: off_hover(select_btn, "lightgray"))

clear_btn = Button(root, text="🗑️ Clear Image", command=clear_image, fg="white", bg="#FF0000", **button_style)
clear_btn.pack(pady=10)
clear_btn.bind("<Enter>", lambda e: on_hover(clear_btn, "#CC0000"))
clear_btn.bind("<Leave>", lambda e: off_hover(clear_btn, "#FF0000"))

root.mainloop()