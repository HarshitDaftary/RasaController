from flask import Flask, request
from AppDelegate import AppDelegate

app = Flask(__name__)

class FlaskWrapper(object):
    
    objAppDelegate = None
    
    def __init__(self):
        print("")
    
    def startServer(self,portNo=5002):
        self.objAppDelegate = AppDelegate()
        app.run(debug=True, port=portNo)
        
@app.route('/json-example')
def json_example():
    print("Received data")
    return 'Done'

@app.route('/', methods=['GET','POST'])

def index():
    objAppDelegate = AppDelegate()
    return "Hello, World!"

