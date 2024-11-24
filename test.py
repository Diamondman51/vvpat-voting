import os
from PIL import Image
import numpy as np


# for img in os.listdir("images/"):
#     photo = Image.open('images/' + img)
#     arr = np.array(photo)
#     print('Shape ', arr)
#     print('Shape ', arr.shape)
#     print('All ', arr.all())
#     with open('test.txt', '+a') as file:
#         file.write(f'{arr}')
#     break

# with open("test.txt", "r") as f:
#     img = f.read()
#     array = np.array([ord(char) for char in img])
#     print("type ", type(array), '\n', array)
#     img = Image.fromarray(img)
#     img.show()







import numpy as np
from PIL import Image

# Read the text file
with open("test.txt", "r") as f:
    img_data = f.read()

# Convert the text to a NumPy array of pixel values (e.g., ASCII values)
array = np.array([ord(char) for char in img_data])  # Convert characters to their ASCII values

# Reshape the array into a 2D format (e.g., a square or rectangular shape)
size = int(np.ceil(np.sqrt(len(array))))  # Calculate the square size
array = np.pad(array, (0, size**2 - len(array)), mode='constant')  # Pad to make it square
array = array.reshape((size, size))

# Create an image from the array
img = Image.fromarray(array.astype('uint8'))  # Ensure data type is uint8
img.show()  # Show the image
