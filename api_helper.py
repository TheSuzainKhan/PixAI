import requests
import time

STABLE_HORDE_KEY = "XAet4KJy9hsXsWcvb7n5_Q"  

API_URL = "https://stablehorde.net/api/v2/generate/async"

def generate_image_from_prompt(prompt, token=None):
    try:
        payload = {
            "prompt": prompt,
            "params": {
                "steps": 25,
                "width": 512,
                "height": 512
            },
            "nsfw": False,
            "censor_nsfw": True
        }

        headers = {
            "apikey": STABLE_HORDE_KEY,
            "Client-Agent": "TkAIImageGeneratorMiniProject:1.0"
        }

        # 1️. Start generation
        start = requests.post(API_URL, headers=headers, json=payload)
        if start.status_code != 202:
            print("API error:", start.status_code, start.text[:200])
            return None

        job_id = start.json().get("id")
        if not job_id:
            print("No job ID received")
            return None

        # 2️. Poll until done
        while True:
            poll = requests.get(f"https://stablehorde.net/api/v2/generate/status/{job_id}")
            data = poll.json()
            if data.get("done"):
                img_url = data["generations"][0]["img"]
                img_data = requests.get(img_url).content
                return img_data
            time.sleep(2)

    except Exception as e:
        print("Exception during API call:", e)
        return None
