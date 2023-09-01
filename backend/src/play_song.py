import time

import mido
from decode_image import decode_image


def play_song_from_encoded_image(image_path: str):
    """
    Plays a song from an encoded image

    :param image_path: the path of the encoded image
    :return:
    """
    # List available MIDI output ports (choose the appropriate one)
    available_ports = mido.get_output_names()
    print("Available MIDI Output Ports:", available_ports)

    # Open a MIDI output port
    outport = mido.open_output(available_ports[0])

    # get the notes to play from the encoded image
    notes = decode_image("encoded_image.png").split(" ")
    notes = [int(note) for note in notes]

    velocity = 64  # Adjust velocity as needed
    duration = 0.5  # Duration of each note in seconds

    # Play the notes
    for note in notes:
        note_on = mido.Message('note_on', note=note, velocity=velocity)
        outport.send(note_on)
        time.sleep(duration)  # Hold the note for the specified duration

        note_off = mido.Message('note_off', note=note, velocity=velocity)
        outport.send(note_off)

    outport.close()


if __name__ == "__main__":
    play_song_from_encoded_image("encoded_image.png")
