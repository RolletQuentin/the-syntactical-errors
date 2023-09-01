import numpy as np
from PIL import Image


def decode_image(image_path):
    """
    Decodes a song message from an image using LSB

    :param image_path: the image to decode
    :return: the decoded song message as a string
    """
    image = Image.open(image_path)

    width, height = image.size
    image_array = np.array(list(image.getdata()))

    # Decode the message
    n = 3 if image.mode == "RGB" else 4
    binary_message = ""
    for p in range((width * height) // n):
        for q in range(0, 3):
            binary_message += (bin(image_array[p][q])[2:][-1])

    binary_message = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]

    # Convert the binary message to a string
    message = ""
    for i in range(len(binary_message)):
        if message[-7:] == "$syntax":
            break
        message += chr(int(binary_message[i], 2))

    return message[:-7]


if __name__ == "__main__":
    print(decode_image("encoded_image.png"))
