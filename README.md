# Mashup Generator (Flask + Streamlit + YouTube Audio)

This project provides web apps (Flask and Streamlit) that generate an audio mashup from YouTube search results and email the result as a ZIP file.

## What the code does

- `app.py` runs a Flask server with two routes:
  - `/` renders a form (see `templates/index.html`).
  - `/submit` accepts form data, generates a mashup, zips it, and emails it to the provided address.
- `streamlit_app.py` provides a Streamlit UI for the same workflow (recommended for Streamlit Cloud deployment).
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
  - streamlit
  - pytubefix
  - moviepy

## Setup

1. Install dependencies:
   ```bash
  pip install -r requirements.txt
   ```
2. Ensure FFmpeg is installed:
   - Windows: install FFmpeg and add it to PATH.
3. Add your email credentials as environment variables:
  - `MASHUP_EMAIL=your_email@gmail.com`
  - `MASHUP_APP_PASSWORD=your_app_password`
  - Use a Gmail App Password, not your normal password.
4. Create a basic form template at `templates/index.html` that posts to `/submit` (already included).

## Run

```bash
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

## Run (Streamlit)

```bash
streamlit run streamlit_app.py
```

Open `http://localhost:8501` in a browser.

On local Windows PowerShell, set secrets before running Streamlit:

```powershell
$env:MASHUP_EMAIL="your_email@gmail.com"
$env:MASHUP_APP_PASSWORD="your_gmail_app_password"
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

### 1. Push to GitHub

Push this project to a GitHub repository with these files at root:
- `streamlit_app.py`
- `102303596.py`
- `requirements.txt`
- `packages.txt`

### 2. Create Streamlit app

1. Go to Streamlit Community Cloud.
2. Click **New app**.
3. Select your repository and branch.
4. Set **Main file path** to `streamlit_app.py`.
5. Deploy.

### 3. Add app secrets

In Streamlit app settings -> **Secrets**, add:

```toml
MASHUP_EMAIL = "your_email@gmail.com"
MASHUP_APP_PASSWORD = "your_gmail_app_password"
```

Important:
- Use a Gmail App Password (Google account with 2FA enabled).
- Do not use your normal Gmail password.

### 4. Why `packages.txt` is included

`moviepy` requires FFmpeg. `packages.txt` ensures Streamlit Cloud installs:
- `ffmpeg`

## Deploy (Recommended: Render with Docker)

This app depends on FFmpeg (`moviepy`), so Docker deployment is the most reliable option.

### 1. Push project to GitHub

Make sure these files are in your repo root:
- `Dockerfile`
- `.dockerignore`
- `app.py`
- `102303596.py`
- `requirements.txt`

### 2. Create a Render Web Service

1. Go to Render dashboard and click **New +** -> **Web Service**.
2. Connect your GitHub repo.
3. Render should detect the `Dockerfile` automatically.
4. Set instance type (Free/Starter is fine to begin).
5. Click **Create Web Service**.

### 3. Set environment variables in Render

In Render service settings, add:
- `MASHUP_EMAIL=your_email@gmail.com`
- `MASHUP_APP_PASSWORD=your_gmail_app_password`

Important:
- Use a Gmail App Password (Google account with 2FA enabled).
- Do not use your normal Gmail password.

### 4. Access your live app

After build and deploy complete, Render gives you a public URL:
- `https://<your-service>.onrender.com`

Open it and test a small mashup request.

## Test Docker locally before deploy

```bash
docker build -t mashup-app .
docker run -p 8000:8000 -e MASHUP_EMAIL=your_email@gmail.com -e MASHUP_APP_PASSWORD=your_app_password mashup-app
```

Then open `http://localhost:8000`.

## Troubleshooting deployment

- If audio processing fails: verify FFmpeg is installed (Dockerfile handles this).
- If mail send fails: verify `MASHUP_EMAIL` and `MASHUP_APP_PASSWORD` are set correctly.
- If request times out: mashups can take a while; this setup uses a longer gunicorn timeout.
- On Streamlit Cloud, keep `packages.txt` in repo root so FFmpeg is installed.

## Notes

- `N` must be greater than 10 and `Y` must be greater than 20 seconds.
- Downloads can take time depending on network and YouTube availability.
- YouTube results and stream availability may change over time.

## Author

Arjun Angirus
