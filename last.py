import cv2
import time
import numpy as np

def overlay_strings_on_video(input_vid, strings, durations):
  # Open the video file
  video = cv2.VideoCapture(input_vid)

  # Loop through the strings and durations
  for string, duration in zip(strings, durations):
    # Set the start time
    start_time = time.time()

    # Loop until the specified duration has elapsed
    while time.time() < start_time + duration:
      # Read the next frame from the video
      success, frame = video.read()

      # Check if we reached the end of the video
      if not success:
        break

      # Get the size of the frame
      height, width, _ = frame.shape

      # Create a black image with the same size as the frame
      overlay = np.zeros((height, width, 3), dtype="uint8")

      # Get the size of the text
      text_width, text_height = cv2.getTextSize(string, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

      # Calculate the coordinates of the text
      x = (width - text_width) // 2
      y = (height - text_height) // 2

      # Draw the text on the black image
      cv2.putText(overlay, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

      # Overlay the text on the frame
      frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)

      # Show the frame
      cv2.imshow("Frame", frame)
      cv2.waitKey(1)

  # Release the video capture
  video.release()

from gtts import gTTS

def text_to_speech(string_list):
    tts_list = []
    for string in string_list:
        tts = gTTS(string, lang='en')
        tts_list.append(tts)
    return tts_list

from playsound import playsound


string_list = ["Hello i am testing the sound"]
# Generate text-to-speech instances
from pydub import AudioSegment

def calculate_duration(tts_list):
    durations = []
    for tts in tts_list:
        # Load the audio file as a pydub AudioSegment
        audio = AudioSegment.from_file(tts.save_to_disk())

        # Calculate the duration in seconds
        duration = len(audio) / 1000
        durations.append(duration)
    return durations



def duration_fn(sentence):
  return 5*len(sentence)
# overlay_strings_on_video("sampleparkour.webm", ["Sentence 1.", "Sentence 2."], [5,5])