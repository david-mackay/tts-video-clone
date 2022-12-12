import cv2
import time
import wave
from io import BytesIO
from gtts import gTTS

def overlay_text(video_file, text, output_file):
    reading_speed = 00
    
    sentences = [sentence.strip() for sentence in text.split(".") if sentence.strip()]
    sentence_durations = [len(sentence) / reading_speed * 60 for sentence in sentences]
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)
    scale = 200
    thickness = 20
    start_position = (100, 300) 
    video = cv2.VideoCapture(video_file)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    total_duration = sum([len(sentence) / reading_speed * 60 for sentence in sentences])
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    max_frames = int(total_frames * total_duration / video.get(cv2.CAP_PROP_FRAME_COUNT))
    start_time = time.time()
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    frame_count = 0
    while frame_count < max_frames:
        elapsed_time = time.time() - start_time
        frame_num = frame_count % total_frames
        if frame_num < total_frames / 2:
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        else:
            video.set(cv2.CAP_PROP_POS_FRAMES, total_frames - frame_num)
        success, frame = video.read()
        if success:
            for i, sentence in enumerate(sentences):
                if elapsed_time >= sum(sentence_durations[:i]):
                    cv2.putText(frame, sentence, start_position, font, scale, color, thickness)
            frame_count += 1
            out.write(frame)
    video.release()
    out.release()

 
overlay_text("sampleparkour.webm", "This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test. This is a test. This is another test.", "output.mp4")