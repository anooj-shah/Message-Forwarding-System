from twilio.rest import Client
import os
import pymongo
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect

app = Flask(__name__)

# MongoDB
mongodb_url = os.environ['MONGO_DB_URL']
DBClient = pymongo.MongoClient(mongodb_url)
db = DBClient['cmh_classes_db']
classes = db['classes']

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


@app.route('/')
def main():
    return 'Message Forwarding System'

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    number = request.values.get('From', None)
    body = request.values.get('Body', None)
    print(body)
    # Start our TwiML response
    resp = MessagingResponse()

    body = body.lower()
    body = body.strip()
    body_arr = body.split()
    class_name = ""
    name = ""
    if len(body_arr) == 4:
        first_name = body_arr[0]
        last_name = body_arr[1]
        name = first_name + " " + last_name
        class_name = body_arr[2] + body_arr[3]
    elif len(body_arr) == 6:
        first_name = body_arr[0]
        last_name = body_arr[1]
        name = first_name + " " + last_name
        class_name = body_arr[2] + body_arr[3] + body_arr[4] + body_arr[5]
    else:
        resp.message("Invalid: Enter your name, class, and session# separated by spaces as shown:\neg: Avi Patel grade1 session1, Ravi Rao PreK session1, Mira Singh kg session2, etc.")
        return str(resp)

    if classes.find_one({'class':class_name}):
        forward_message(class_name, number, name)
        resp.message("Your teachers have been notified")

    else:
        resp.message("Invalid: Enter your name, class, and session# separated by spaces as shown:\neg: Avi Patel grade1 session1, Ravi Rao PreK session1, Mira Singh kg session2, etc.")

    return str(resp)

def forward_message(class_name, number, name):
    class_dict = classes.find_one({'class':class_name})
    phone_numbers = class_dict['phone_numbers']
    message_body = "Your student " + name + " (" + number + ") is requesting entry into the class " + class_name
    for i in phone_numbers:
        message = client.messages.create(body=message_body, from_='+12816669996', to=i[1])
        print(message.sid)

if __name__ == '__main__':
    app.run()
