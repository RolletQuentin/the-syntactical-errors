import numpy as np
from PIL import Image

def decode_image(image_path: str) -> str:
    """
    Decodes a song message from an image using LSB

    :param image_path: the image to decode
    :return: the decoded song message as a string
    """
    img = Image.open(image_path, 'r')
    image_array = np.array(list(img.getdata()))

    channel_num = 3 if img.mode == "RGB" else 4
    total_pixels = image_array.size // channel_num

    lsb_count = 1
    lsb_count_detected = False
    binary_message = ""
    for pixel in range(total_pixels):
        for current_channel in range(0, channel_num):
            # Convert given bit into binary, slice off integer indication and get last char
            lsb_index = -lsb_count
            current_lsb = bin(image_array[pixel][current_channel])[2:][-lsb_index]

            # Get LSB count if not done yet, otherwise concatenate to binary_message.
            if lsb_count_detected:
                binary_message += current_lsb
            elif current_lsb == "0":
                lsb_count_detected = True
            else:
                lsb_count += 1

            print("Current LSB index: ", lsb_index, " ", "Current LSB count: ", lsb_count, end="\r")

    # Convert message to list of bits
    binary_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]

    # Check binary for delimiter, and stop writing to message when this happens
    message = ""
    for i in range(len(binary_message)):
        if message[-7:] == "$syntax":
            break
        message += chr(int(binary_message[i], 2))

    img.close()
    return message[:-7]

if __name__ == "__main__":
    print(decode_image("encoded_image.png"))
