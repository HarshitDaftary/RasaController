from User.User import User

class Medium(object):

    arrUsers = []
    objSnipsWrapper = None

    def __init__(self):
        print("Medium Initialised")

    def processIncomingMessage(self,dictIncomingMessage):
        print("Incoming message called")

    def sendMessageBack(self,objUser,strMessage):
        print("send message to this user")