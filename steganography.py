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
    secret_message = password + "|" + secret_message + "====="
    binary_message = to_bin(secret_message)
    msg_len = len(binary_message)

    img = image.copy()
    total_pixels = img.size

    if msg_len > total_pixels:
        raise ValueError("Message too long to fit in the image!")

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
            binary_data += r[-1] + g[-1] + b[-1]

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data.endswith("====="):
            break

    decoded_data = decoded_data.replace("=====", "")
    saved_password, actual_message = decoded_data.split("|", 1)
    return actual_message if saved_password == password else None

# --- MAIN ---
# Ask user for image path instead of using absolute local path
img_path = input("Enter image path (e.g., assets/mypic.jpg): ")
image = cv2.imread(img_path)
if image is None:
    print("Error: Could not load image.")
    exit()

secret_msg = input("Enter secret message: ")
passwd = input("Enter a passcode: ")

encoded_image = encode_message(image, secret_msg, passwd)
output_path = "assets/encryptedImage.png"
cv2.imwrite(output_path, encoded_image)
print(f"Message hidden in {output_path}")

try:
    os.startfile(output_path)
except:
    pass

dec_pass = input("Enter passcode for decryption: ")
decoded_message = decode_message(cv2.imread(output_path), dec_pass)

if decoded_message:
    print("Decrypted message:", decoded_message)
else:
    print("Wrong password. Access denied.")
