from flask import Flask, render_template, request, flash
import smtplib
import os

### SMTP ARGS ###
SMTP_HOST = 'smtp.mailtrap.io'
SMTP_PORT = 587
SMTP_USERNAME = 'd6f6e81a51fa39'
SMTP_PASSWORD = '2769eb75e0fc0c';
EMAIL_FROM = 'mailtrap@altacarbon.eco'
EMAIL_TO = 'brandon.flannery@altacarbon.eco'
#################

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        data = request.form
        data = request.form
        print(data)
        send_email(data["name"], data["email"], data["subject"], data["message"])
        return render_template('contactsuccess.html')
    else:
        return app.send_static_file('index.html')


def send_email(name, email, subject, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nSubject: {subject}\nMessage:{message}"
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(SMTP_USERNAME, SMTP_PASSWORD)
        connection.sendmail(EMAIL_FROM, EMAIL_TO, email_message)


if __name__ == '__main__':
    app.run(threaded=True, port=4121)



