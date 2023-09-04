import random
import time
import numpy as np
from PIL import Image
from scipy.io import wavfile

def encode_wav(image_path: str, song_path: str, output_path: str, lsb_count: int = 2) -> None:
    """
    Encodes a wavfile into an image using LSB

    :param image_path: path of the image to encode
    :param song_path: path of song to encode
    :param output_path: path of the output image
    :return:
    :throws: ValueError if the image is not large enough to hold the message
    """
    # TODO: Remove debug print statements when done
    image = Image.open(image_path)

    # Create numpy array with list of all pixels in image
    width, height = image.size
    image_array = np.array(list(image.getdata()))

    # Get wavfile data and put it onto a string seperated by spaces
    print("Before wavfile read")
    sample_rate, audio_data = wavfile.read(song_path)
    audio_data = " ".join(str(i) for i in audio_data)
    print("Data length: ",len(audio_data))
    song_message = str(sample_rate)+" "+audio_data
    print("After wavfile read")
    
    # Prepare LSB metadata
    # Why is the LSB count stored this way? Given that there will never be more than 8 LSBs, and a space is another bit, this uses less space.
    lsb_digit_count = lsb_count-1
    time_before_binary_convert = time.time()
    lsb_metadata = "1"*lsb_digit_count+"0"
    lsb_metadata_length = len(lsb_metadata)
    lsb_start_index = 9

    # Convert the message to binary and add a delimiter
    song_message += "$syntax"
    binary_message = lsb_metadata+"".join([format(ord(i), "08b") for i in song_message])
    
    binary_message_length = len(binary_message)
    print("Time to convert to binary: ",time.time()-time_before_binary_convert)
    print("Binary message length: ",binary_message_length)

    # Check if the image is large enough to hold the message
    channel_num = 3 if image.mode == "RGB" else 4
    if binary_message_length > width * height * channel_num:
        raise ValueError("The image is not large enough to hold the message")

    # Encode the message
    time_before_encoding = prev_iter_time = time.time()
    index = 0
    for pixel in image_array:
        for i in range(0, channel_num):
            if index < binary_message_length:
                # Changes pixel colour code into binary, removes integer indication and adds message at current index
                pixel[i] = int(bin(pixel[i])[2:lsb_start_index] + binary_message[index], 2)
                index += 1

                if lsb_metadata_length == index:
                    lsb_start_index = 10-lsb_count

                # Calculate total time remaining
                current_time = time.time()
                remaining_total_time = int((current_time-prev_iter_time)*(binary_message_length-index))
                print("At index: ", index," ", "Total remaining time: ", remaining_total_time, end="\r")
                prev_iter_time = current_time

    print("Time after encoding: ",time.time()-time_before_encoding)

    # Save the image
    image_array = image_array.reshape(height, width, channel_num)
    encoded_image = Image.fromarray(image_array.astype('uint8'), image.mode)
    encoded_image.save(output_path)

    encoded_image.close()
    image.close()
    print("Image encoded successfully")

def random_notes_test(length: int = 2000, min_max: tuple[int, int] = (21, 108)) -> str:
    """
    Function to test how the image will look when given a large amount of data to encode.
    """
    result = ""
    for i in range(length):
        result += str(random.randint(min_max[0], min_max[1]))+" "
    print(result)
    
    return result

def binary_read_test(file_path: str) -> bytes:
    """
    Testing reading files as binary
    """
    with open(file_path, "rb") as file:
        binary_data = file.read()

    return binary_data

if __name__ == "__main__":
    encode_wav("Screenshot 2023-07-21 125828.png", "rickroll-1s.wav", "encoded_image.png")
    #encode_wav("Screenshot 2023-07-21 125828.png", "rickroll.wav", "encoded_image.png")
