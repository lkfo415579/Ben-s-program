#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, json, request, Response
from urllib import unquote
import sys, cgi

print 'Server ready!'

app = Flask(__name__)

@app.route("/translate", methods=['POST', 'GET'])
def translate():
	if not request.json:
		abort(400)
	print 'Received new task [POST]', request.json
	data = request.json
	
	try:
		return Response(json.dumps({'text': 'ok'}, encoding='utf-8', ensure_ascii=False, indent=4), mimetype='application/javascript')
	except:
		return Response(json.dumps({'text': 'fail'}, encoding='utf-8', ensure_ascii=False, indent=4), mimetype='application/javascript')

if __name__ == "__main__":
	app.run(host='10.119.186.29', port=8088)
