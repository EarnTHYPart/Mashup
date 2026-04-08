import os
import zipfile
import smtplib
from email.message import EmailMessage
import importlib.util
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
MASHUP_PATH = BASE_DIR / "102303596.py"

spec = importlib.util.spec_from_file_location("mashup_script", str(MASHUP_PATH))
mashup_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mashup_module)
create_mashup = mashup_module.create_mashup


def get_secret(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    if name in st.secrets:
        return st.secrets[name]
    return ""


def send_email_with_zip(receiver_email: str, zip_filename: Path) -> None:
    sender_email = get_secret("MASHUP_EMAIL")
    app_password = get_secret("MASHUP_APP_PASSWORD")

    if not sender_email or not app_password:
        raise ValueError(
            "Missing credentials. Add MASHUP_EMAIL and MASHUP_APP_PASSWORD in Streamlit secrets."
        )

    msg = EmailMessage()
    msg["Subject"] = "Music Mashup Result - Arjun Angirus (102303596)"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Attached is the zip file containing your mashup.")

    with open(zip_filename, "rb") as file_obj:
        msg.add_attachment(
            file_obj.read(),
            maintype="application",
            subtype="zip",
            filename="102303596_mashup.zip",
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)


def cleanup_temp_files() -> None:
    for file_path in BASE_DIR.glob("temp_*.mp4"):
        file_path.unlink(missing_ok=True)
    for file_path in BASE_DIR.glob("temp_audio_*.mp3"):
        file_path.unlink(missing_ok=True)


st.set_page_config(page_title="Audio Mashup Builder", page_icon="🎵", layout="centered")
st.title("Audio Mashup Builder")
st.write("Generate a YouTube audio mashup and email the ZIP result.")

with st.form("mashup_form"):
    singer = st.text_input("Singer or keyword", placeholder="Arijit Singh")
    num_videos = st.number_input("Number of videos (N)", min_value=11, value=12, step=1)
    duration = st.number_input("Clip duration in seconds (Y)", min_value=21, value=25, step=1)
    receiver_email = st.text_input("Email to receive the mashup", placeholder="you@example.com")
    submitted = st.form_submit_button("Generate mashup")

if submitted:
    if not singer.strip():
        st.error("Please enter a singer name or keyword.")
    elif not receiver_email.strip():
        st.error("Please enter an email address.")
    else:
        output_mp3 = BASE_DIR / "102303596-output.mp3"
        zip_file = BASE_DIR / "102303596-mashup.zip"

        try:
            with st.spinner("Creating mashup... this can take a couple of minutes."):
                create_mashup(singer.strip(), int(num_videos), int(duration), str(output_mp3))

                if not output_mp3.exists() or output_mp3.stat().st_size == 0:
                    raise RuntimeError("Mashup file was not created. Try different input values.")

                with zipfile.ZipFile(zip_file, "w") as zip_obj:
                    zip_obj.write(output_mp3, arcname=output_mp3.name)

                send_email_with_zip(receiver_email.strip(), zip_file)

            st.success(f"Success! Mashup ZIP has been sent to {receiver_email.strip()}.")
        except Exception as err:
            st.error(f"Error: {err}")
        finally:
            output_mp3.unlink(missing_ok=True)
            zip_file.unlink(missing_ok=True)
            cleanup_temp_files()

st.caption("Note: N must be greater than 10 and Y must be greater than 20 seconds.")
