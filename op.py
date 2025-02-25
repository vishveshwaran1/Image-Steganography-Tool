import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np

def encode_message(image_path, message, output_path):
    image = Image.open(image_path).convert("RGBA")
    message += "###"  # Delimiter to indicate the end of the message
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    pixels = np.array(image)
    flat_pixels = pixels.flatten()
    
    if len(binary_message) > len(flat_pixels):
        messagebox.showerror("Error", "Message is too long to encode in this image.")
        return
    
    for i in range(len(binary_message)):
        flat_pixels[i] = (flat_pixels[i] & ~1) | int(binary_message[i])
    
    pixels = flat_pixels.reshape(pixels.shape)
    encoded_image = Image.fromarray(pixels)
    encoded_image.save(output_path, "PNG")
    messagebox.showinfo("Success", "Message successfully encoded!")

def decode_message(image_path):
    image = Image.open(image_path)
    pixels = np.array(image)
    flat_pixels = pixels.flatten()
    
    binary_message = ''.join(str(pixel & 1) for pixel in flat_pixels)
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''.join(chr(int(char, 2)) for char in chars)
    
    if "###" in decoded_message:
        return decoded_message.split("###")[0]
    return "No hidden message found."

def select_image(entry):
    file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def encode_gui():
    input_path, output_path, message = input_entry.get(), output_entry.get(), message_entry.get("1.0", tk.END).strip()
    if not input_path or not output_path or not message:
        messagebox.showerror("Error", "All fields must be filled.")
        return
    encode_message(input_path, message, output_path)

def decode_gui():
    input_path = decode_entry.get()
    if not input_path:
        messagebox.showerror("Error", "Please select an image.")
        return
    hidden_message = decode_message(input_path)
    messagebox.showinfo("Decoded Message", hidden_message)

# GUI Setup
root = tk.Tk()
root.title("Steganography Tool")
root.configure(bg="#2c3e50")
root.geometry("500x350")

header_font = ("Arial", 14, "bold")
label_font = ("Arial", 10)
button_font = ("Arial", 10, "bold")

# Encoding Section
tk.Label(root, text="Encode Message into Image", font=header_font, bg="#2c3e50", fg="white").grid(row=0, columnspan=3, pady=10)

tk.Label(root, text="Input Image:", font=label_font, bg="#2c3e50", fg="white").grid(row=1, column=0, padx=10, pady=5)
input_entry = tk.Entry(root, width=40)
input_entry.grid(row=1, column=1, pady=5)
tk.Button(root, text="Browse", font=button_font, command=lambda: select_image(input_entry)).grid(row=1, column=2, padx=5)

tk.Label(root, text="Output Image:", font=label_font, bg="#2c3e50", fg="white").grid(row=2, column=0, padx=10, pady=5)
output_entry = tk.Entry(root, width=40)
output_entry.grid(row=2, column=1, pady=5)
tk.Button(root, text="Browse", font=button_font, command=lambda: output_entry.insert(0, filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")]))) .grid(row=2, column=2, padx=5)

tk.Label(root, text="Message:", font=label_font, bg="#2c3e50", fg="white").grid(row=3, column=0, padx=10, pady=5)
message_entry = tk.Text(root, height=4, width=30)
message_entry.grid(row=3, column=1, columnspan=2, pady=5)

tk.Button(root, text="Encode", font=button_font, bg="#27ae60", fg="white", command=encode_gui).grid(row=4, columnspan=3, pady=10)

# Decoding Section
tk.Label(root, text="Decode Message from Image", font=header_font, bg="#2c3e50", fg="white").grid(row=5, columnspan=3, pady=10)

tk.Label(root, text="Encoded Image:", font=label_font, bg="#2c3e50", fg="white").grid(row=6, column=0, padx=10, pady=5)
decode_entry = tk.Entry(root, width=40)
decode_entry.grid(row=6, column=1, pady=5)
tk.Button(root, text="Browse", font=button_font, command=lambda: select_image(decode_entry)).grid(row=6, column=2, padx=5)

tk.Button(root, text="Decode", font=button_font, bg="#e74c3c", fg="white", command=decode_gui).grid(row=7, columnspan=3, pady=10)

root.mainloop()
