
from flask import Flask, request
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAATkVXLTakQBO3f6CsSXKWqZAcgmGdfc22xhFHjTBp4h75MtzCkIZB58ZAIZBHxBa7VJlZC0ZCkfdGHOn2zeSXZCDjmmjnxESs2PXbtN5QGsQRbDr2lHTEEJYEuJlwCZBCmwMusMulZAJn0VFdb8m21y7FKetIhFsbg2sVyebhaMieaqGRTlRL4J00LlMPY4AZBI17'
VERIFY_TOKEN = 'joeiiaa'

def send_message(recipient_id, message_text, image_url):
    url = 'https://graph.facebook.com/v18.0/me/messages'
    params = {'access_token': PAGE_ACCESS_TOKEN}
    headers = {'Content-Type': 'application/json'}
    
    # Send text
    text_data = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text}
    }
    requests.post(url, params=params, headers=headers, json=text_data)
    
    # Send image
    image_data = {
        'recipient': {'id': recipient_id},
        'message': {
            'attachment': {
                'type': 'image',
                'payload': {'url': image_url, 'is_reusable': True}
            }
        }
    }
    requests.post(url, params=params, headers=headers, json=image_data)

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification token mismatch"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data.get("entry", []):
        messaging = entry.get("messaging", [])
        for message_event in messaging:
            sender_id = message_event['sender']['id']
            if 'message' in message_event:
                send_message(sender_id, "أهلاً وسهلاً! 👋", "https://i.imgur.com/Ou6tYcD.jpg")
    return "ok", 200

if __name__ == '__main__':
    app.run(port=5000)
