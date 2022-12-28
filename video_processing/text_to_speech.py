import requests
import json
import asyncio
import wave
import contextlib

import requests

def convert_text_to_audio(sentences):
    """Convert a list of sentences to audio files using a remote endpoint.
    
    Args:
        sentences: A list of strings, where each string is a sentence to be converted to audio.
    
    Returns:
        A list of URLs pointing to the audio files.
    """

    url = "https://play.ht/api/v1/convert"


    headers = {
    'Authorization': 'f41bf92f26f44b8f956dca54e943cd52',
    'X-User-ID': 'wYr7N3UdspX5W933fyfPRELrk4S2',
    'Content-Type': 'application/json'
    }
    # Initialize an empty list to store the audio file URLs
    audio_urls = []
    
    # Loop through each sentence
    for sentence in sentences:
        # Set the JSON payload for the current sentence
        payload = json.dumps({
        "voice": "Larry",
        "content": sentence,
        "speed": "1.0",
        "preset": "balanced"
        })
        
        # Send the POST request
        response = requests.post(ENDPOINT_URL, json=payload, headers=headers)
        
        # If the request was successful, add the audio file URL to the list
        if response.status_code == 200:
            audio_urls.append(response.json()["audio_url"])
        
        # If the request was not successful, raise an error
        else:
            raise Exception("Request failed with status code {}".format(response.status_code))
    
    # Return the list of audio file URLs
    return audio_urls

import requests

def download_audio_files(urls):
    """Download audio files from the given URLs and store them in a list.
    
    Args:
        urls: A list of strings, where each string is a URL for an audio file.
    
    Returns:
        A list of bytestrings containing the audio file data.
    """
    # Initialize an empty list to store the audio file data
    audio_data = []
    
    # Loop through the URLs
    for url in urls:
        # Send a GET request to download the audio file
        response = requests.get(url)
        
        # If the request was successful, add the audio file data to the list
        if response.status_code == 200:
            audio_data.append(response.content)
        
        # If the request was not successful, raise an error
        else:
            raise Exception("Request failed with status code {}".format(response.status_code))
    
    # Return the list of audio file data
    return audio_data



def get_audio_duration(audio_data):
    """Determine the duration of an audio file from its data.
    
    Args:
        audio_data: A bytestring containing the data of the audio file.
        
    Returns:
        The duration of the audio file in seconds.
    """
    # Open the audio data as a wave file
    with contextlib.closing(wave.open(io.BytesIO(audio_data))) as f:
        # Get the frame rate and number of frames
        frame_rate = f.getframerate()
        num_frames = f.getnframes()
        
        # Calculate the duration in seconds
        duration = num_frames / frame_rate
        
        return duration

async def request_tts(content):
    url = "https://play.ht/api/v1/convert"

    payload = json.dumps({
    "voice": "Larry",
    "content": content,
    "speed": "1.0",
    "preset": "balanced"
    })
    headers = {
    'Authorization': 'f41bf92f26f44b8f956dca54e943cd52',
    'X-User-ID': 'wYr7N3UdspX5W933fyfPRELrk4S2',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response


# print(convert_text_to_audio(["This is a test", "this is the second sentence of the test...!"]))