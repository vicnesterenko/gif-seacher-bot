import os
import urllib.parse

import requests
from fastapi import FastAPI, Request

TOKEN = os.getenv("TOKEN", "")  # in Spacefile
HOST = os.getenv("DETA_SPACE_APP_HOSTNAME", "")

BOT_API = f"https://api.telegram.org/bot{TOKEN}"
WEBHOOK_PATH = "/webhook"  # also in Spacefile public_routes


def _https(url: str) -> str:
    """Prepend https:// to url"""

    p = urllib.parse.urlparse(url)
    return p._replace(
        scheme="https",
        netloc=(p.netloc or p.path),
        path=(p.path if p.netloc else ""),
    ).geturl()


def send_msg(chat_id, text):
    return requests.post(
        f"{BOT_API}/sendMessage",
        json={"chat_id": chat_id, "text": text},
    ).json()


def get_random_gif_url(search_obj):
    URL = "https://api.giphy.com/v1/gifs/search"
    API_KEY = "GiFp2ffdGXNciyoQVRTWtMZogRbmzgua"

    PARAMETERS = {
        "api_key": API_KEY,
        "q": search_obj,
        "limit": 3,
        "offset": 3,
        "rating": "g",
        "lang": "en",
        "bundle": "messaging_non_clips",
    }

    response = requests.get(URL, params=PARAMETERS)

    if response.status_code == 200:
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            gif_urls = [item["images"]["original"]["url"] for item in data["data"]]
            return gif_urls
        else:
            return []
    else:
        return []


# APP

app = FastAPI()


@app.get("/")
def home():
    """Shows webhook info (optional)"""
    resp = requests.get(f"{BOT_API}/getWebhookInfo")
    return resp.json()


@app.get("/setup")
def setup():
    """Sets webhook url on bot (optional)"""
    resp = requests.get(
        f"{BOT_API}/setWebHook",
        params={"url": urllib.parse.urljoin(_https(HOST), WEBHOOK_PATH)},
    )
    return resp.json()


@app.get("/forget")
def forget():
    """Removes webhook url from bot (optional)"""
    resp = requests.get(f"{BOT_API}/deleteWebhook")
    return resp.json()


@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()

    chat_id = data["message"]["chat"]["id"]

    # Check if the "text" key exists in the message
    if "text" in data["message"]:
        prompt = data["message"]["text"]
        gif_url = get_random_gif_url(prompt)

        if prompt.startswith("/start"):
            msg = "\n".join(
                [
                    "Hi dear!💖",
                    "Write what gif you want.",
                ]
            )
        elif prompt.startswith("/stop"):
            msg = "Bye, dear user. See you soon. When you come back, write /start command!"
        else:
            if gif_url:
                # Construct a message with GIF links
                msg = "\n".join(
                    [
                        f"Link {i}: {gif_url}"
                        for i, gif_url in enumerate(gif_url, start=1)
                    ]
                )
            else:
                msg = "\n".join(
                    [
                        f"Sorry, no GIFs found for search '{prompt}'😢",
                        "Please try again.",
                        "Write what gif you want next or edit your previous search.",
                    ]
                )

    elif "sticker" in data["message"]:
        msg = "\n".join(["Received a sticker 🌟", "Write what gif you want."])
    elif "photo" in data["message"] or "video" in data["message"]:
        msg = "\n".join(
            [
                "Received a photo 📸 or video 🎥!",
                "Write what gif you want.",
            ]
        )
    else:
        msg = "\n".join(["Received a non-text message.", "Write what gif you want."])

    return send_msg(chat_id, msg)
