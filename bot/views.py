import os
import json
import random
import requests

from django.shortcuts import render
from django.http import HttpResponse

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def index(request):
    return HttpResponse("It works!")

def callback(request_json):
    reply = ""
#    request_json = request_json_origin.body.POST["events"]
    request = json.loads(request_json.body.decode('utf-8'))
    for e in request["events"]:
        reply_token = e["replyToken"]
        if e["type"] == "message":
            if e["message"]["type"] == "text":
                reply += e["message"]["text"]
            else:
                reply += "only text message"
            reply_message(reply_token, reply)
    return HttpResponse(reply)

def make_text():
    from . import reply_words
    return random.choice(reply_words)


def reply_message(reply_token, reply):
    reply_body = {
        "replyToken":reply_token,
        "messages":[
            {
                "type":"text",
                "text": reply
            }
        ]
    }
    r = requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(reply_body))
    print(r.)

