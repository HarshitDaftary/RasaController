
# coding: utf-8

# In[2]:


from flask import Flask, request

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
    return "Hello, World!"



# In[3]:


class AppDelegate(object):
    arrChannels = []
    
    def __init__(self):
        print("Initialized")


# In[4]:


class Channel(object):
    arrUsers = []
    
    def __init__(self):
        print("")


# In[5]:


class User(object):
    arrMessages = []
    
    def __init__(self):
        print("")


# In[6]:


class Message(object):
    strText = ""
    
    def __init__(self):
        print("")


# In[7]:


objFlaskWrapper = FlaskWrapper()
objFlaskWrapper.startServer()

