"""
Yoto Jungle Adventure — Live Streaming Server
 
Each game picks a random story and tracks the player's
path through the tree based on which knob they turn.

Endpoints:
  GET /welcome    — intro audio, picks a story, starts session
  GET /story      — current story node narration + choice prompt
  GET /left       — player turned right knob back (first choice)
  GET /right      — player turned right knob forward (second choice)
  GET /ending     — final story ending

Card chapter layout:
  Chapter 1: /welcome
  Chapter 2: /story    (track 1)
  Chapter 3: /left     (track 1) — player navigates here for left choice
  Chapter 4: /right    (track 1) — player navigates here for right choice
  Chapter 5: /ending

"""

import os
import random
import time
import logging
import requests
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

from stories import STORIES

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

app = FastAPI(title="Yoto Adventure Server")

# CONFIG
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
VOICE_ID           = os.getenv("YOTO_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
ELEVENLABS_URL     = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

# SESSION STORE
# { player_id: { story, node_key, depth, ended } }
sessions: dict[str, dict] = {}

MAX_DEPTH = 5   # number of choices before story ends


def new_session(player_id: str) -> dict:
    story = random.choice(STORIES)
    session = {
        "story":    story,
        "node_key": "1",
        "depth":    0,
        "ended":    False,
        "started":  time.time(),
    }
    sessions[player_id] = session
    log.info(f"New session: player={player_id} story='{story['title']}'")
    return session


def get_session(player_id: str) -> dict | None:
    return sessions.get(player_id)


def current_node(session: dict) -> dict:
    return session["story"]["nodes"][session["node_key"]]


# TTS
def tts_stream(text: str):
    log.info(f"TTS ({len(text)} chars): {text[:80]}...")
    resp = requests.post(
        ELEVENLABS_URL,
        headers={
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {
                "stability":        0.55,
                "similarity_boost": 0.75,
            },
        },
        stream=True,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.iter_content(chunk_size=4096)


def audio(text: str) -> StreamingResponse:
    return StreamingResponse(tts_stream(text), media_type="audio/mpeg")

# PLAYER ID
def player_id(request: Request) -> str:
    return (
        request.headers.get("x-yoto-device-id")
        or request.headers.get("x-device-id")
        or request.client.host
        or "default"
    )


# CHOICE PROMPT
def choice_prompt(node: dict) -> str:
    return (
        f"Turn the right knob forward to {node['left']}. "
        f"Or turn it back to {node['right']}."
    )


# ROUTES

@app.get("/welcome")
async def welcome(request: Request):
    """Start a new game — pick a random story and play the intro."""
    pid     = player_id(request)
    session = new_session(pid)
    story   = session["story"]
    node    = current_node(session)

    text = (
        f"Welcome to Jungle Adventure! "
        f"Today's story is: {story['title']}. "
        f"{story['intro']} "
        f"Turn the right knob forward when you're ready to begin!"
    )
    return audio(text)


@app.get("/story")
async def story(request: Request):
    """Read the current story node and present the choice."""
    pid     = player_id(request)
    session = get_session(pid)

    if not session:
        session = new_session(pid)

    node = current_node(session)

    # If we're at an ending node, redirect to the ending
    if node.get("ending"):
        return audio(
            f"{node['text']} Turn the right knob forward to hear how your adventure ends!"
        )

    remaining = MAX_DEPTH - session["depth"]
    if remaining == 1:
        depth_hint = "This is your last choice, make it count!"
    elif remaining == 2:
        depth_hint = "You are nearly at the end of your adventure."
    else:
        depth_hint = ""

    prompt = choice_prompt(node)
    text   = f"{node['text']} {depth_hint} {prompt}".strip()
    return audio(text)


@app.get("/left")
async def go_left(request: Request):
    """Player turned the left knob — advance story left."""
    return _advance(request, direction="left")


@app.get("/right")
async def go_right(request: Request):
    """Player turned the right knob — advance story right."""
    return _advance(request, direction="right")


def _advance(request: Request, direction: str) -> StreamingResponse:
    pid     = player_id(request)
    session = get_session(pid)

    if not session:
        return audio("Hmm, I've lost track of your adventure. Turn the right knob forward to start over!")

    node = current_node(session)

    if node.get("ending"):
        return audio("Your adventure is already complete! Turn the right knob forward to hear the ending.")

    # Move to next node
    next_key = node.get(f"{direction}_node")
    if not next_key:
        return audio("I couldn't find that path through the jungle. Turn the right knob forward to try again.")

    session["node_key"] = next_key
    session["depth"]   += 1

    next_node = current_node(session)

    # Acknowledge the choice briefly then read next node
    chosen_action = node["left"] if direction == "left" else node["right"]
    acknowledgement = f"You chose to {chosen_action.lower()}. "

    if next_node.get("ending"):
        # We've reached an ending
        session["ended"] = True
        text = (
            f"{acknowledgement}"
            f"{next_node['text']} "
            f"Turn the right knob forward to finish your adventure!"
        )
    else:
        prompt = choice_prompt(next_node)
        text   = f"{acknowledgement}{next_node['text']} {prompt}"

    return audio(text)


@app.get("/ending")
async def ending(request: Request):
    """Play the final ending and close the session."""
    pid     = player_id(request)
    session = get_session(pid)

    if not session:
        return audio("Insert the card again to start a brand new jungle adventure!")

    node = current_node(session)

    if node.get("ending"):
        ending_type = node.get("ending_type", "triumph")
        if ending_type == "triumph":
            outro = "What an amazing adventure! You should be very proud. Insert the card again for a brand new story!"
        elif ending_type == "mishap":
            outro = "Things didn't go quite to plan — but that's what makes a great story! Try again for a different ending!"
        else:  # surprise
            outro = "What a wonderfully unexpected adventure! The jungle is full of surprises. Insert the card again to discover another!"
        text = f"{node['text']} {outro}"
    else:
        text = (
            "Your adventure isn't finished yet — "
            "go back and keep making choices! "
            "Turn the right knob forward or back to continue your story."
        )

    sessions.pop(pid, None)
    return audio(text)

# HEALTH
@app.get("/health")
async def health():
    return {
        "status":        "ok",
        "stories":       len(STORIES),
        "active_sessions": len(sessions),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
