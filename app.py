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
# post = {'class':'Test', 'phone_numbers':['+345']}
# classes.insert_one(post)
#


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

    # Determine the right reply for this message
    if body == "test":
        forward_message(number)
        resp.message("Your teachers have been notified")

    else:
        resp.message("Invalid message: please enter your class and session # (ex: class1 session1):")
    return str(resp)

def forward_message(number):
    class_dict = classes.find_one({'class':'Test'})
    phone_numbers = class_dict['phone_numbers']
    message_body = "Your student " + number + " is requesting entry into the class"
    for i in phone_numbers:
        message = client.messages.create(body=message_body, from_='+14783471874', to=i)
        print(message.sid)

if __name__ == '__main__':
    app.run()
