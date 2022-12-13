import requests
import json


def request_tts(content):
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

print(request_tts(["This is a test"]))