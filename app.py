from twilio.rest import Client
import os
import pymongo
from flask import Flask

app = Flask(__name__)

# MongoDB
# DBClient = pymongo.MongoClient("mongodb+srv://anooj101:cmhtest@cmhclasses-s7bby.gcp.mongodb.net/test?retryWrites=true&w=majority")
# db = DBClient['cmh_classes_db']
# classes = db['classes']
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
    return 'Hello, World!'

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello':
        resp.message("Hi!")
    elif body == 'bye':
        resp.message("Goodbye")

    return str(resp)


if __name__ == '__main__':
    app.run()
