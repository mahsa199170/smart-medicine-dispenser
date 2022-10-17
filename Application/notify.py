# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=broad-except
# pylint: disable=line-too-long

import os
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def notify(name, contact, email, string):

    notify_string = ""

    if string != "":
        app_string = string.split("#")
        if app_string[0] == "False":
            notify_string = "Hello! " + name + ", Your appointment has been confirmed for " + app_string[1]
        else:
            notify_string = "Hello! " + name + ", Your appointment has been changed to " + app_string[1]
    else:
        notify_string = 'Hello! ' + name + ', Kindly reach out to the medicine dispenser to take your medicine'

    contact = '+1' + contact
    account_sid = 'AC064abe68031a2563740447d37b5827ec'
    auth_token = '2519a44e44cfd4957e8893fb58e0eb72'
    client = Client(account_sid, auth_token)

    client.messages.create(
        messaging_service_sid='MG3a998c5ddb3da15cb5432e88e49fbd07',
        body=notify_string,
        to=contact
        )

    client.calls.create(
        twiml='<Response><Say>' + notify_string + '</Say></Response>',
        to=contact,
        from_='+14156340921'
        )

    message = Mail(
        from_email='smart.medicine.dispenser.smd@gmail.com',
        to_emails=email,
        subject='Medicine Reminder/Confirmation',
        html_content='<strong>' + notify_string + '</strong>')
    try:
        send = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        send.send(message)
    except Exception as error:
        print(error)
