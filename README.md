# Mashup Generator (Flask + YouTube Audio)

This project provides a small Flask web app that generates an audio mashup from YouTube search results and emails the result as a ZIP file.

## What the code does

- `app.py` runs a Flask server with two routes:
  - `/` renders a form (expects `templates/index.html`).
  - `/submit` accepts form data, generates a mashup, zips it, and emails it to the provided address.
- `102303596.py` contains the mashup logic:
  - Searches YouTube for the singer/keyword.
  - Downloads audio from the first `N` videos.
  - Cuts the first `Y` seconds from each audio clip.
  - Concatenates all clips into one MP3.

## How it works (flow)

1. User submits singer name, number of videos `N`, clip duration `Y` (seconds), and email.
2. The server calls `create_mashup()` to download and stitch audio.
3. The output MP3 is saved, zipped, and sent via Gmail SMTP.

## Requirements

- Python 3.9+
- FFmpeg installed and on PATH (required by moviepy)
- Packages:
  - Flask
  - pytubefix
  - moviepy

## Setup

1. Install dependencies:
   ```bash
   pip install flask pytubefix moviepy
   ```
2. Ensure FFmpeg is installed:
   - Windows: install FFmpeg and add it to PATH.
3. Set your email credentials in `app.py`:
   - `YOUR_EMAIL@gmail.com`
   - `YOUR_APP_PASSWORD`
   - Use a Gmail App Password, not your normal password.
4. Create a basic form template at `templates/index.html` that posts to `/submit`.

## Run

```bash
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

## Notes

- `N` must be greater than 10 and `Y` must be greater than 20 seconds.
- Downloads can take time depending on network and YouTube availability.
- YouTube results and stream availability may change over time.
