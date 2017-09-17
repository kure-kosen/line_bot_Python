import os
import json
import random
import requests

from django.shortcuts import render
from django.http import HttpResponse
from load_words import reply_words

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = os.environ("LINE_ACCESS_TOKEN")
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}


def index(request):
    return HttpResponse("This is bot api.")


def callback(request):
	reply = ""
	request_json = json.loads(request.body.decode('utf-8'))
	for e in request_json['events']:
		reply_token = e['reply_Token']
		message_type = e['message']['type']

		if message_type == 'text':
			text = e['message']['text']
			reply += make_text()
		else:
			reply += "今はテキストのみ返信できます"

		reply_text(reply_token, reply)

	return HttpResponse(reply)


def make_text():
	return random.choice(reply_words)


def reply_text(reply_token, reply):
	payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": reply
                }
            ]
    }

	requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload))
