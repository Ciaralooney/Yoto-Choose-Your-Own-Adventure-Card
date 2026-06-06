"""
This needs to be run once to create the MYO card.
This will add the streaming track URLs to the card. 
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

YOTO_ACCESS_TOKEN = os.getenv("YOTO_ACCESS_TOKEN")
SERVER_URL        = os.getenv("SERVER_URL")
CARD_TITLE        = "Jungle Adventure!"
LABS_API          = "https://labs.api.yotoplay.com/content/job"
VOICE_ID          = os.getenv("YOTO_VOICE_ID_STORY")

ICONS_BASE    = "https://raw.githubusercontent.com/Ciaralooney/Yoto-Choose-Your-Own-Adventure-Card/main/images"
ICON_WELCOME  = f"{ICONS_BASE}/hello.png"
ICON_STORY    = f"{ICONS_BASE}/book.png"
ICON_CHOICE1  = f"{ICONS_BASE}/choice_one.png"
ICON_CHOICE2  = f"{ICONS_BASE}/choice_two.png"
ICON_ENDING   = f"{ICONS_BASE}/star.png"


def headers():
    return {
        "Authorization": f"Bearer {YOTO_ACCESS_TOKEN}",
        "Content-Type":  "application/json",
    }


def stream_track(key, title, endpoint, label, icon, duration=25):
    base = SERVER_URL.rstrip("/")
    return {
        "key":          key,
        "title":        title,
        "trackUrl":     f"{base}/{endpoint}",
        "type":         "stream",
        "overlayLabel": label,
        "display":      {"icon16x16": icon},
        "format":       "mp3",
        "duration":     duration,
        "fileSize":     0,
        "channels":     "stereo",
    }


def build_structure():
    """
    Chapter 1: Welcome / new game
    Chapter 2: Current story node
    Chapter 3: Left choice
    Chapter 4: Right choice
    Chapter 5: Ending
    """
    return {
        "title": CARD_TITLE,
        "content": {
            "chapters": [
                {
                    "key": "01", "title": "Welcome", "display": {"icon16x16": ICON_WELCOME},
                    "tracks": [stream_track("01", "Welcome", "welcome", "▶", ICON_WELCOME, duration=40)],
                },
                {
                    "key": "02", "title": "Story", "display": {"icon16x16": ICON_STORY},
                    "tracks": [stream_track("01", "Story", "story", "📖", ICON_STORY, duration=30)],
                },
                {
                    "key": "03", "title": "First Choice", "display": {"icon16x16": ICON_CHOICE1},
                    "tracks": [stream_track("01", "First Choice", "left", "←", ICON_CHOICE1, duration=30)],
                },
                {
                    "key": "04", "title": "Second Choice", "display": {"icon16x16": ICON_CHOICE2},
                    "tracks": [stream_track("01", "Second Choice", "right", "→", ICON_CHOICE2, duration=30)],
                },
                {
                    "key": "05", "title": "Ending", "display": {"icon16x16": ICON_ENDING},
                    "tracks": [stream_track("01", "Ending", "ending", "★", ICON_ENDING, duration=40)],
                },
            ]
                },
            ]
        },
        "metadata": {
            "title":       CARD_TITLE,
            "description": "A branching jungle adventure, different story every time!",
        },
    }


def main():

    card_id = sys.argv[1] if len(sys.argv) > 1 else None
    content = build_structure()
    if card_id:
        content["cardId"] = card_id
        print(f"Updating card: {card_id}")
    else:
        print("Creating new card...")

    resp = requests.post(
        f"{LABS_API}?voiceId={VOICE_ID}",
        headers=headers(),
        json=content,
    )

    if not resp.ok:
        print(f"❌ {resp.status_code} {resp.text}")
        sys.exit(1)

    job = resp.json().get("job", {})
    print(f"Card submitted! Job ID: {job.get('jobId')}")
    print(f"\n Find it in the Yoto app → My Cards → '{CARD_TITLE}'")
    print(f"   Link it to a blank MYO card and you're done.")
    print(f"\nServer: {SERVER_URL}")


if __name__ == "__main__":
    main()