from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_emails():
    data = request.json
    smtp_server = data.get('smtp_server')
    smtp_port = int(data.get('smtp_port'))
    email_user = data.get('email_user')
    email_password = data.get('email_password')
    recipients = data.get('recipients') # List of emails
    subject = data.get('subject')
    message_body = data.get('message')

    success_count = 0
    failed = []

    try:
        # Connect to SMTP Server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)

        for recipient in recipients:
            recipient = recipient.strip()
            if not recipient:
                continue
            
            try:
                msg = MIMEMultipart()
                msg['From'] = email_user
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(message_body, 'plain'))

                server.send_message(msg)
                success_count += 1
            except Exception as e:
                failed.append(f"{recipient}: {str(e)}")
            
            # Small delay to be polite to the server
            time.sleep(0.5)

        server.quit()
        
        return jsonify({
            'status': 'completed',
            'success_count': success_count,
            'failed': failed
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
