import cv2
import numpy as np
import os

def to_bin(data):
    """Convert data to binary format."""
    if isinstance(data, str):
        return ''.join([format(ord(i), '08b') for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, '08b') for i in data]
    elif isinstance(data, int):
        return format(data, '08b')
    else:
        raise TypeError("Type not supported.")

def encode_message(image, secret_message, password):
    # Combine password + message
    secret_message = password + "|" + secret_message
    # Add a delimiter to mark end of message
    secret_message += "====="
    
    # Convert to binary
    binary_message = to_bin(secret_message)
    msg_len = len(binary_message)

    # Get image copy
    img = image.copy()
    total_pixels = img.size

    if msg_len > total_pixels:
        raise ValueError("Message is too long to fit in the image!")

    data_index = 0
    for row in img:
        for pixel in row:
            r, g, b = to_bin(pixel)
            if data_index < msg_len:
                pixel[0] = int(r[:-1] + binary_message[data_index], 2)
                data_index += 1
            if data_index < msg_len:
                pixel[1] = int(g[:-1] + binary_message[data_index], 2)
                data_index += 1
            if data_index < msg_len:
                pixel[2] = int(b[:-1] + binary_message[data_index], 2)
                data_index += 1
            if data_index >= msg_len:
                break
    return img

def decode_message(image, password):
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    
    # Split into 8-bit bytes
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data.endswith("====="):
            break

    decoded_data = decoded_data.replace("=====", "")
    saved_password, actual_message = decoded_data.split("|", 1)

    if saved_password == password:
        return actual_message
    else:
        return None

# === MAIN ===
# Load image
img_path = r"C:\Users\Divya\Desktop\cyber\mypic.jpg"  # Change to your image path
image = cv2.imread(img_path)
if image is None:
    print("Error: Could not load image.")
    exit()

# Input
secret_msg = input("Enter secret message: ")
passwd = input("Enter a passcode: ")

# Encode
encoded_image = encode_message(image, secret_msg, passwd)
output_path = "encryptedImage.png"
cv2.imwrite(output_path, encoded_image)
print(f"Message hidden in {output_path}")

# Automatically open the image
os.startfile(output_path)

# Decode
dec_pass = input("Enter passcode for decryption: ")
decoded_message = decode_message(cv2.imread(output_path), dec_pass)

if decoded_message:
    print("Decrypted message:", decoded_message)
else:
    print("Wrong password. Access denied.")
