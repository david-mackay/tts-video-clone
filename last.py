import cv2
import time
import numpy as np
import textwrap
import boto3
from math import ceil
from video_processing.separate_sentences import *
from content_generation.text_grabber import grab_top_posts


def overlay_strings_on_video(input_vid, strings, durations):
  video = cv2.VideoCapture(input_vid)
  print(durations)

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

      # Wrap the text to a maximum width
      wrap_width = 50
      wrapped_text = textwrap.wrap(string, wrap_width)

      # Calculate the coordinates of the text
      text_width, text_height = cv2.getTextSize(string, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

      # Keep track of the longest line of text in the wrapped text
      max_line_width = 0
      total_text_height = 0
      # Loop through the wrapped text and calculate the longest line
      for line in wrapped_text:
        line_width, _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        _, line_height = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        total_text_height += line_height

        max_line_width = max(max_line_width, line_width)

      # Calculate the x coordinate based on the width of the longest line
      x = (width - max_line_width) // 2

      # Calculate the y coordinate based on the total height of the wrapped text
      y = (height - total_text_height) // 2

      # Draw the wrapped text on the overlay
      for line in wrapped_text:
        cv2.putText(overlay, line, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        y += line_height+10


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





def duration_fn(sentence):
  return ceil(0.4*len(sentence.split(" ")))

# sentences = split_on_new_lines(separate_string(grab_top_posts("WritingPrompts", 6)))
# overlay_strings_on_video("sampleparkour.webm", sentences, [duration_fn(x) for x in sentences])

converts = text_to_speech(["hello.", "my name is poop."])

import wave
import os

def get_length_in_seconds(filenames):
    duration = [] 
    for filename in filenames:
        with wave.open(filename, 'rb') as audio_file:
            num_frames = audio_file.getnframes()
            frame_rate = audio_file.getframerate()
            length_in_seconds = num_frames / frame_rate
            duration.append(length_in_seconds)
    return duration

# filenames = ['file1.wav', 'file2.wav', 'file3.wav']
# total_length = get_length_in_seconds(filenames)
# print(total_length)  # Outputs the total length in seconds


def tts_polly(text):
  # Send a request to the Amazon Polly TTS service to synthesize speech
  # with sentence duration information
  client = boto3.client('polly')
  response = client.synthesize_speech(
      Text=text,
      VoiceId='Matthew',
      OutputFormat='mp3',
      SpeechMarkTypes=['sentence']
  )

  # Get the synthesized speech task and wait for it to complete
  task = response['SynthesisTask']
  task_arn = task['TaskArn']
  client.get_speech_synthesis_task(TaskArn=task_arn)

  # Get the duration of each sentence in the synthesized speech
  response = client.get_speech_synthesis_task(TaskArn=task_arn)
  result = response['SynthesisTask']['TaskStatus']
  while result == 'inProgress' or result == 'scheduled':
      response = client.get_speech_synthesis_task(TaskArn=task_arn)
      result = response['SynthesisTask']['TaskStatus']

  sentence_durations = response['SynthesisTask']['SentenceLengths']
  return result, sentence_durations
  # print(sentence_durations)  # Outputs a list of sentence durations in seconds


print(tts_polly("Hey I am testing. is this cool? Monkey man."))


