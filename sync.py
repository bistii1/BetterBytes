import requests
import time

SYNC_API_KEY = "sk-mK8iGkWIRRmBD9tYZO9fYA.aaKVGjQ-IeqGvzws6tTqSOblh32VHPbj"

def generate_lip_sync(voice_id, text, input_video_url):
    url = "https://api.sync.so/v2/generate"

    payload = {
        "model": "lipsync-1.9.0-beta",
        "input": [
            {
                "type": "text",
                "provider": {
                    "name": "elevenlabs",
                    "voiceId": voice_id,
                    "script": text
                }
            },
            {
                "type": "video",
                "url": input_video_url
            }
        ],
        "options": {
                "pads": [0, 5, 0, 0],
                "speedup": 1,
                "output_format": "mp4",
                "sync_mode": "bounce",
                "fps": 25,
                "output_resolution": [1280, 720],
                "active_speaker": True
        }
    }
    headers = {
        "x-api-key": SYNC_API_KEY,
        "Content-Type": "application/json"
    }

    print("request options:", payload)

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        json_response = response.json()
        video_id = json_response.get("id")
        print("Response ID:", video_id)

        return poll_for_output_url(video_id)

    except Exception as err:
        print("Fetch error:", err)
        raise

def poll_for_output_url(video_id):
    """Polls the API until the output URL is ready."""
    poll_url = f"https://api.sync.so/v2/generate/{video_id}"
    print(poll_url)
    headers = {
        "x-api-key": SYNC_API_KEY,
        "Content-Type": "application/json"
    }

    while True:
        response = requests.get(poll_url, headers=headers)
        print("status code:", response.status_code)
        
        json_response = response.json()
        status = json_response.get("status")
        print("status 2 ", status)
        if status == "COMPLETED":
            output_url = json_response.get("outputUrl")
            output_dur = json_response.get("outputDuration")
            print("Output Duration:", output_dur)
            print("Lip-sync video ready:", output_url)
            return output_url
        elif status == "failed":
            print("Lip-sync processing failed.")
            return None
        elif status == "PENDING" or status == "PROCESSING":
            print("Lip-sync video still processing...")
            #print(f"Error polling: {response.status_code} - {response.text}")
            time.sleep(5)
            continue

#print("POST Response:", response.json())

#response = requests.request("GET", url, headers=headers)

#if response.status_code == 200:
    time.sleep(2)
    print("loading get response")  # Print the processed JSON response
#else:
    print(f"GET Request failed with status code {response.status_code}: {response.text}")