import time
import argparse
import boto3
from tts_video_clone.entry_points.parse_text import replace_aita
parser = argparse.ArgumentParser(prog='synthesize_speech')
parser.add_argument('-i', '--input_text', type=str, help='file path to the text file')
parser.add_argument('-t', '--story_type', type=str, help='type of video')
args = parser.parse_args()


def synthesize_speech(text_file: str, story_type: str):
    with open(text_file, 'r') as f:
        text = f.read()
        if story_type == "aita":
            text = replace_aita(text)
    # Send a request to the Amazon Polly TTS service to synthesize speech
    # with sentence duration information
    client = boto3.client('polly')

        # speech_mark_response = client.start_speech_synthesis_task(
        #     Text=text,
        #     VoiceId='Ruth',
        #     OutputFormat='json',
        #     Engine='neural',
        #     SpeechMarkTypes=['sentence'],
        #     OutputS3BucketName="reddit-tts-python"
        # )
    audio_response = client.start_speech_synthesis_task(
        Text=text,
        VoiceId='Matthew',
        OutputFormat='mp3',
        Engine='neural',
        OutputS3BucketName="reddit-tts-python"
    )

    # Get the synthesized speech task and wait for it to complete
    # # print(response)
    # speech_mark_info = speech_mark_response['SynthesisTask']
    audio = audio_response['SynthesisTask']

    while client.get_speech_synthesis_task(TaskId=audio["TaskId"])["SynthesisTask"]["TaskStatus"] != "completed":
        print("waiting..")
        time.sleep(2)

    # print(speech_mark_info["OutputUri"])
    print(audio["OutputUri"])
    return 0


synthesize_speech(args.input_text, args.story_type)
