import numpy as np
from PIL import Image

def encode_image(image_path: str, song_message: str, output_path: str):
    """
    Encodes a song message into an image using LSB

    :param image_path: path of the image to encode
    :param song_message: message to encode (currently it has to be passed as a string of numbers separated by spaces)
    :param output_path: path of the output image
    :return:
    :throws: ValueError if the image is not large enough to hold the message
    """
    image = Image.open(image_path)

    width, height = image.size
    image_array = np.array(list(image.getdata()))

    # Convert the message to binary and add a delimiter
    song_message += "$syntax"
    binary_message = "".join([format(ord(i), "08b") for i in song_message])
    binary_message_length = len(binary_message)

    # Check if the image is large enough to hold the message
    n = 3 if image.mode == "RGB" else 4
    if binary_message_length > width * height * n:
        raise ValueError("The image is not large enough to hold the message")

    # Encode the message
    index = 0
    for pixel in image_array:
        for i in range(0, n):
            if index < binary_message_length:
                # Changes pixel colour code into binary, removes integer indication and adds message at current index
                pixel[i] = int(bin(pixel[i])[2:9] + binary_message[index], 2)
                index += 1

    # Save the image
    image_array = image_array.reshape(height, width, n)
    encoded_image = Image.fromarray(image_array.astype('uint8'), image.mode)
    encoded_image.save(output_path)

    print("Image encoded successfully")


if __name__ == "__main__":
    encode_image("Screenshot 2023-07-21 125828.png", "60 62 64 65 67 69 71 72", "encoded_image.png")
