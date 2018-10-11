from Medium.Medium import Medium
from User.WebUser import WebUser
import json

class WebMedium(Medium):

    dictPendingMessage = {}

    def processIncomingMessage(self, dictIncomingmessage):

        strTmpSessionId = dictIncomingmessage['session_id']
        strUserMessage = dictIncomingmessage['data']['message']
        objUser = self.findUser(strTmpSessionId)
        objUser.userSentMessage(strUserMessage)

    def findUser(self,strTmpSessionId):
        for objUser in self.arrUsers:
            if objUser.strSessionId == strTmpSessionId:
                return objUser

        objTmpUser = WebUser()
        objTmpUser.strSessionId = strTmpSessionId 
        objTmpUser.objSnipsWrapper = self.objSnipsWrapper
        objTmpUser.objCurrentMedium = self
        objTmpUser.updateUserMetadata()
        self.arrUsers.append(objTmpUser)
        return objTmpUser

    def sendMessageBack(self,objUser,strMessage):
        print("message from NLP")
        print(strMessage)

        if objUser.strSessionId in self.dictPendingMessage and self.dictPendingMessage[objUser.strSessionId] != None:
            arrPendingMessages = self.dictPendingMessage[objUser.strSessionId]
            arrPendingMessages.append(strMessage)
        else:
            arrPendingMessages = []
            arrPendingMessages.append(strMessage)
            self.dictPendingMessage[objUser.strSessionId] = arrPendingMessages

    def getPendingMessages(self,dictIncomingmessage):

        strTmpSessionId = dictIncomingmessage['session_id']
        objUser = self.findUser(strTmpSessionId)

        if objUser.strSessionId in self.dictPendingMessage and self.dictPendingMessage[objUser.strSessionId] != None:
            arrPendingMessages = self.dictPendingMessage[objUser.strSessionId]

            arrMessage = []
            for strMessage in arrPendingMessages:
                dictMessage = {}
                dictMessage["type"] = "text"
                dictMessage["message"] = strMessage
                arrMessage.append(dictMessage.copy())
            
            del arrPendingMessages[:]
            return json.dumps(arrMessage)
        else:
            return ""