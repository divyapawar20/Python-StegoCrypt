import cv2
import os
import string

# Read the image
img = cv2.imread("mypic.jpg")

# Get the secret message and password from the user
msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Create dictionaries for character-to-ASCII and ASCII-to-character mappings
d = {}
c = {}
for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)

# Initialize variables for embedding the message
m = 0
n = 0
z = 0

# Embed the message into the image
for i in range(len(msg)):
    img[n, m, z] = d[msg[i]]
    n = n + 1
    m = m + 1
    z = (z + 1) % 3

# Save the encrypted image
cv2.imwrite("encryptedImage.jpg", img)

# Open the encrypted image
os.system("start encryptedImage.jpg")

# Get the passcode for decryption
pas = input("Enter passcode for Decryption: ")

# Decrypt the message if the passcode is correct
if password == pas:
    message = ""
    n = 0
    m = 0
    z = 0
    for i in range(len(msg)):
        message = message + c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    print("Decryption message: ", message)
else:
    print("YOU ARE NOT auth")