from flask import Flask, render_template, request, flash
from flask_login import login_required, current_user
from flask import Blueprint
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


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        data = request.form
        data = request.form
        print(data)
        send_email(data["name"], data["email"], data["subject"], data["message"])
        return render_template('contactsuccess.html')
    else:
        return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


def send_contact_form_email(name, email, subject, message):
    """
    Sends an email using the SMTP host defined in global variables above

        Args:
            name (str): Name of sender of contact form
            email (str): Email address of sender of form
            subject (str): Subject of contact form message
            message (str): Message of contact form


        Raises:
            None

        Returns:
            None
    """
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nSubject: {subject}\nMessage:{message}"
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(SMTP_USERNAME, SMTP_PASSWORD)
        connection.sendmail(EMAIL_FROM, EMAIL_TO, email_message)




