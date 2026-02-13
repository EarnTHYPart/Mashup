from flask import Flask, render_template, request
import os
import zipfile
import smtplib
from email.message import EmailMessage
import importlib.util

app = Flask(__name__)

# Load mashup module
script_dir = os.path.dirname(os.path.abspath(__file__))
mashup_path = os.path.join(script_dir, "102303596.py")
spec = importlib.util.spec_from_file_location("mashup_script", mashup_path)
mashup_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mashup_module)
create_mashup = mashup_module.create_mashup

def send_email_with_zip(receiver_email, zip_filename):
    sender_email = os.getenv("MASHUP_EMAIL")
    app_password = os.getenv("MASHUP_APP_PASSWORD")
    if not sender_email or not app_password:
        raise ValueError("Missing email credentials. Set MASHUP_EMAIL and MASHUP_APP_PASSWORD.")
    msg = EmailMessage()
    msg['Subject'] = 'Music Mashup Result - Arjun Angirus (102303596)'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content('Attached is the zip file containing your mashup.')

    with open(zip_filename, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='zip', filename='102303596_mashup.zip')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    singer = request.form['singer']
    n = int(request.form['num_videos'])
    dur = int(request.form['duration'])
    email = request.form['email']
    
    output_mp3 = "102303596-output.mp3"
    zip_file = "102303596-mashup.zip"

    try:
        create_mashup(singer, n, dur, output_mp3)
        
        with zipfile.ZipFile(zip_file, 'w') as z:
            z.write(output_mp3)
        
        send_email_with_zip(email, zip_file)
        
        return f"<h2>Success!</h2><p>Mashup zip file has been sent to <b>{email}</b>.</p>"
    except Exception as e:
        return f"<h2>Error!</h2><p>{str(e)}</p>"

if __name__ == '__main__':

    app.run(debug=True)