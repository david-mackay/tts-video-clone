import cv2
import time
import numpy as np
import textwrap
import boto3
import json
from math import ceil

from content_generation.text_grabber import grab_top_posts
from video_processing.separate_sentences import separate_string, split_on_new_lines


def overlay_strings_on_video(input_vid, strings, durations):
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
                y += line_height + 10

            # Overlay the text on the frame
            frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)

            # Show the frame
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)

    # Release the video capture
    video.release()


# filenames = ['file1.wav', 'file2.wav', 'file3.wav']
# total_length = get_length_in_seconds(filenames)
# print(total_length)  # Outputs the total length in seconds


def speech_synthesize_polly(text):
    # Send a request to the Amazon Polly TTS service to synthesize speech
    # with sentence duration information
    client = boto3.client('polly')

    speech_mark_response = client.start_speech_synthesis_task(
        Text=text,
        VoiceId='Matthew',
        OutputFormat='json',
        Engine='neural',
        SpeechMarkTypes=['sentence'],
        OutputS3BucketName="reddit-tts-python"
    )
    audio_response = client.start_speech_synthesis_task(
        Text=text,
        VoiceId='Matthew',
        OutputFormat='mp3',
        Engine='neural',
        OutputS3BucketName="reddit-tts-python"
    )

    # Get the synthesized speech task and wait for it to complete
    # print(response)
    speech_mark_info = speech_mark_response['SynthesisTask']
    audio = audio_response['SynthesisTask']

    while client.get_speech_synthesis_task(TaskId=audio["TaskId"])["SynthesisTask"]["TaskStatus"] != "completed":
        print("waiting..")
        time.sleep(2)

    print(speech_mark_info["OutputUri"])
    print(audio["OutputUri"])
    # Create an S3 client


def get_durations_from_speechmarks(filename: str, total_length):
    timestamps = []
    sentences = []
    with open(filename, 'r') as f:
        for i in f:
            data = json.loads(i)
            timestamps.append(data["time"])
            sentences.append(data["value"])
    return _get_intervals(timestamps, total_length), sentences


def _get_intervals(data, total_length):
    intervals = []
    for i in range(len(data) - 1):
        interval = data[i + 1] - data[i]
        intervals.append(interval)
    intervals.append(total_length - data[-1])
    return intervals

    # for item in data:
    #   print(item)


def overlay_strings_on_video2(input_vid, output_vid, strings, durations):
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
                y += line_height + 10

            # Overlay the text on the frame
            frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)

            out.write(frame)

        # Release the video capture and VideoWriter objects
    video.release()
    out.release()


# posts = grab_top_posts("WritingPrompts", 3, 3)


# speech_synthesize_polly(posts)
durations, sentences = get_durations_from_speechmarks("speechmarks.marks", 789013)
overlay_strings_on_video2("minecraft1.mp4", "output2.mp4", sentences, durations)
duration = [x / 1000 for x in durations]
# overlay_strings_on_video("minecraft1.mp4", sentences, duration)

# print(get_durations_from_speechmarks("speechmarks.txt", 3000))
