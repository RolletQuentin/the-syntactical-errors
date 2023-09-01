import numpy as np
from PIL import Image


def decode_image(image_path: str):
    """
    Decodes a song message from an image using LSB

    :param image_path: the image to decode
    :return: the decoded song message as a string
    """
    img = Image.open(image_path, 'r')
    image_array = np.array(list(img.getdata()))

    n = 3 if img.mode == "RGB" else 4
    total_pixels = image_array.size // n

    binary_message = ""
    for pixel in range(total_pixels):
        for i in range(0, n):
            binary_message += (bin(image_array[pixel][i])[2:][-1])

    binary_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]

    message = ""
    for i in range(len(binary_message)):
        if message[-7:] == "$syntax":
            break
        message += chr(int(binary_message[i], 2))

    return message[:-7]


if __name__ == "__main__":
    print(decode_image("encoded_image.png"))
