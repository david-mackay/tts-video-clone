# Import the necessary modules
import cv2
import numpy as np
from typing import List

def display_sentences_over_video(sentences: List[str], input_filename: str, output_filename: str) -> None:
  # Read the input video
  video = cv2.VideoCapture(input_filename)

  # Get the video dimensions
  video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
  video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

  # Create a VideoWriter object to write the output video
  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  out = cv2.VideoWriter(output_filename, fourcc, 20.0, (video_width, video_height))

  for sentence in sentences:
    # Clear the previous sentence

    # Create a black image with the same dimensions as the video
    img = np.zeros((video_height, video_width, 3), np.uint8)

    # Get the size of the text
    text_size = cv2.getTextSize(sentence, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

    # Calculate the position of the text
    text_x = (video_width - text_size[0]) // 2
    text_y = (video_height + text_size[1]) // 2

    # Put the text in the center of the image
    cv2.putText(img, sentence, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    # Show the image with the text over the video
    cv2.imshow("Video with text", img)

    # Write the image to the output video file
    out.write(img)

    # Wait for a key press
    cv2.waitKey(0)

  # Release the VideoCapture and VideoWriter objects
  video.release()
  out.release()

sentences = ["Test1.", "Test2."]

display_sentences_over_video(sentences, "sampleparkour.webm", "output.mp4")