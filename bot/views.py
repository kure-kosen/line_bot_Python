import os
import json
import random
import requests

from django.shortcuts import render
from django.http import HttpResponse

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN") #セキュリティの観点から環境変数に設定
HEADER = {
	"Content-Type": "application/json",
	"Authorization": "Bearer " + ACCESS_TOKEN
}


def index(request):
	return HttpResponse(request)


def callback(request_json):
	reply = ""
	request = json.loads(request_json.read().decode('utf-8'))
	for e in request['events']:
		reply_token = e['reply_Token']

		if e['type'] == "message":
			if e['message']['type'] == "text":
				reply += make_text()
			else:
				reply += "今はテキストのみ返信できます"

		reply_message(reply_token, reply)

	return HttpResponse(reply)


def make_text():
	from . import reply_words
	return random.choice(reply_words)


def reply_message(reply_token, reply):
	reply_body = {
        	'replyToken':reply_token,
        	'messages':[
                	{
                    		'type':"text",
                    		'text': reply
                	}
            	]
    	}

	requests.post(REPLY_ENDPOINT, headers=HEADER, body=json.dumps(reply_body))

