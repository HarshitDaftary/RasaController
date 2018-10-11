import os
from flask import Flask, request #import main Flask class and request object
from AppDelegate import AppDelegate
import json

app = Flask(__name__) #create the Flask app

objAppDelegate = AppDelegate()

class FlaskWrapper:

    def __init__(self):        
        print('initialisation of Flask')  

    def startFlaskServer(self):
        objAppDelegate.startNLUServers()
        app.run(debug=True, port=5002)

@app.route('/json-example')
def json_example():
    print("Received data")
    return 'Todo...'

@app.route('/chat_app',methods = ['GET', 'POST'])
def chat_app():
    print("in Chat app Received --",json.dumps(request.json))
    
    if request.form:
        output = dict(request.form)
        
    if request.json:
        output = dict(request.json)
        text = json.loads(json.dumps(request.json))
        return objAppDelegate.processWebMessage(text)