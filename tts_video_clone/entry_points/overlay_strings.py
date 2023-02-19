import argparse
import textwrap

import cv2
import numpy as np

from tts_video_clone.durations import get_durations_from_speechmarks

parser = argparse.ArgumentParser(prog='overlay_strings')

parser.add_argument('-i', '--input_vid', type=str, help='file path to the input_vid file')
parser.add_argument('-o', '--output_vid', type=str, help='file path to the output_vid file')
parser.add_argument('-d', '--duration', type=str, help='file path to the duration speechmarks file')
parser.add_argument('-l', '--length', type=int, help='total_length in ms')
args = parser.parse_args()


def overlay_strings(input_vid, output_vid, strings, durations):
    video = cv2.VideoCapture(input_vid)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_vid, fourcc, fps,
                          (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    # Loop through the strings and durations
    for string, duration in zip(strings, durations):
        # Calculate the number of frames to show the text for
        num_frames = int(duration * fps / 1000)

        # Loop through the number of frames
        for i in range(num_frames):
            # Read the next frame from the video
            success, frame = video.read()

            # Check if we reached the end of the video
            if not success:
                break

            # Get the size of the frame
            height, width, _ = frame.shape

            # Create a black image with the same size as the frame
            overlay = np.zeros((height, width, 3), dtype="uint8")

            # Wrap the text to a maximum width
            wrap_width = 50
            wrapped_text = textwrap.wrap(string, wrap_width)

            # Calculate the coordinates of the text
            text_width, text_height = cv2.getTextSize(string, cv2.FONT_HERSHEY_TRIPLEX, 1.5, 2)[0]

            # Keep track of the longest line of text in the wrapped text
            max_line_width = 0
            total_text_height = 0
            # Loop through the wrapped text and calculate the longest line
            for line in wrapped_text:
                line_width, _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_TRIPLEX, 1.5, 2)[0]
                _, line_height = cv2.getTextSize(line, cv2.FONT_HERSHEY_TRIPLEX, 1.5, 2)[0]
                total_text_height += line_height

                max_line_width = max(max_line_width, line_width)

            # Calculate the x coordinate based on the width of the longest line
            x = (width - max_line_width) // 2

            # Calculate the y coordinate based on the total height of the wrapped text
            y = (height - total_text_height) // 2

            # Draw the wrapped text on the overlay
            for line in wrapped_text:
                _, line_height = cv2.getTextSize(line, cv2.FONT_HERSHEY_TRIPLEX, 1.5, 2)[0]
                cv2.putText(overlay, line, (x, y), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255, 255, 255), 2)
                y += line_height + 10

            # Overlay the text on the frame
            frame = cv2.addWeighted(overlay, 0.75, frame, 0.5, 0)

            out.write(frame)

        # Release the video capture and VideoWriter objects
    video.release()
    out.release()
    return 0


durations, strings = get_durations_from_speechmarks(args.duration, args.length)
overlay_strings(args.input_vid, args.output_vid, strings, durations)
