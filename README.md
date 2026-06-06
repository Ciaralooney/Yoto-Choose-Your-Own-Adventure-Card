# Yoto Jungle Adventure

A branching audio adventure game for the Yoto player.
A different story every time, turn the knobs to choose your path.

---

## How to play

```
Insert card → Welcome + story intro plays
Turn the right knob → story begins

At each choice point:
  Turn the LEFT knob  → take that path
  Turn the RIGHT knob → take the other path

After 5 choices → your ending plays
Insert the card again → completely new story!
```

## What's included

- **3 complete stories** with 5 decision points each (16 possible endings per story)
- **48 unique ending paths** across all stories
- Stories pick randomly on each card insert

Stories included:
1. **The Lost Baby Elephant**, help a baby elephant find its herd
2. **The Stolen River Stone**, chase a mischievous otter and discover jungle magic  
3. **The Night the Jungle Went Dark**, find the missing firefly queen before morning


## Setup

### 1. Install
 - Search for command prompt
 - Right click on it and choose run as admin
 - CD to your project folder
 - Run:
```bash
pip install -r requirements.txt
```

### 2. Get API Keys and create your .env file
**ElevenLabs** (for text-to-speech):
- Sign up at [elevenlabs.io](https://elevenlabs.io) 
- Copy your API key from [here](https://elevenlabs.io/app/developers/api-keys)

**Yoto**:
- Go to [dashboard.yoto.dev](https://dashboard.yoto.dev) and create an app

- Follow the [Headless/CLI auth guide](https://yoto.dev/authentication/headless-cli-auth/) to get an access token OR go to https://github.com/Ciaralooney/Yoto-Access-Token-Generator for a simpler way to do this


Make an .env file and fill in `ELEVENLABS_API_KEY`, `YOTO_VOICE_ID_STORY` and `YOTO_ACCESS_TOKEN`.

## Deploy the server
You need this running somewhere permanently. What I suggest:

### Render
1. Push your project version to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Set start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
4. Add env vars in the Render dashboard

## Build the card
Once your server is deployed:

1. Add `SERVER_URL=example.com` to your `.env` You will find your project URL on the Render dashboard.
2. Run:
```bash
python build_card.py
```
Then in the Yoto app: My Cards → "Jungle Adventure!" → link to a blank MYO card.
 
## Adding more stories

Edit `stories.py`. Each story is a dict with:
- `title` , read aloud at the start
- `intro` , scene-setting paragraph
- `nodes` , dict of story nodes, root key always `"1"`

Each non-ending node needs:
```python
"node_key": {
    "text":       "Narration for this moment in the story.",
    "left":       "Short description of left choice",
    "right":      "Short description of right choice",
    "left_node":  "key_of_next_node",
    "right_node": "key_of_next_node",
}
```

Each ending node needs:
```python
"node_key": {
    "text":         "The ending narration.",
    "ending":       True,
    "ending_type":  "triumph",  # or "mishap" or "surprise"
}
```

Node keys follow the path: `"1"` → `"1L"` / `"1R"` → `"1LL"` / `"1LR"` / `"1RL"` / `"1RR"` → etc.

## Updating the card

If you ever change your server URL, rebuild the card:
```bash
python build_card.py <your-existing-card-id>
```
Card ID is visible in the Yoto app URL when viewing the card.
