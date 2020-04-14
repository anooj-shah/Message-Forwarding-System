from twilio.rest import Client
import os
import pymongo
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect

app = Flask(__name__)

# MongoDB
DBClient = pymongo.MongoClient("mongodb+srv://anooj101:cmhtest@cmhclasses-s7bby.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = DBClient['cmh_classes_db']
classes = db['classes']
# # post = {'class':'Test', 'phone_numbers':['+18326006867']}
# # classes.insert_one(post)
#
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# message = client.messages.create(body='Hi there!', from_='+14783471874',to='+18326006867')
#
# print(message.sid)

@app.route('/')
def main():
    return 'Message Forwarding System'

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    print(body)
    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == "test":
        forward_message()
        resp.message("Your teachers have been notified")

    else:
        resp.message("Invalid message: please enter your class and session # (ex: class1 session1):")

    return str(resp)

def forward_message():
    class_dict = classes.find_one({'class':'Test'})
    phone_numbers = class_dict['phone_numbers']
    for i in phone_numbers:
        message = client.messages.create(body='Hi there!', from_='+14783471874',to=i)
        print(message.sid)

forward_message()
if __name__ == '__main__':
    app.run()
