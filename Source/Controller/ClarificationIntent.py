import random
import sys
import os
import io
import json
from Controller.IntentController import IntentController
from IntentMapper import IntentMapper
from NLP.TextBlobNLPWrapper.TextBlobWrapper import TextBlobWrapper

script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir, "NLP/SnipsNLUWrapper/sample_dataset.json")
with io.open(path) as f:
    sample_dataset = json.load(f)

class ClarificationIntentController(object):

    objCurrentIntent = None   # Instance of IntentController
    objCurrentUser = None
    objIntentMapper = IntentMapper()
    objSnipsWrapper = None
    intClarificationCounter = 0
    objTextBlobWrapper = TextBlobWrapper()

    def __init__(self):
        print("Initialisation of clarification intent")

    def askClarification(self,strMessage):

        strIntentName = self.objCurrentIntent.intentId
        self.intClarificationCounter = self.intClarificationCounter + 1

        if 'clarification_messages' in sample_dataset['intents'][strIntentName]:
            arrClarificationMessages = sample_dataset['intents'][strIntentName]['clarification_messages']
            intIndex = random.randint(0,len(arrClarificationMessages)-1)
            strMessage = arrClarificationMessages[intIndex]
            self.objCurrentUser.current_state = 3 
            self.objCurrentUser.messageFromIntent(self.objCurrentIntent,strMessage)
        else:
            self.objCurrentUser.current_state = 3 
            strMessage = "Sorry I could not get you. Please elaborate"
            self.objCurrentUser.messageFromIntent(self.objCurrentIntent,strMessage)

    def userAnswered(self,strMessage):
        dictParsedData = self.objSnipsWrapper.parse(strMessage)
            
        if dictParsedData["intent"] != None:
            print("could detect an intent")
            strIntentName = dictParsedData["intent"]["intentName"]
            fltConfidence = dictParsedData["intent"]["probability"]

            objController = self.objIntentMapper.getObjectForIntentId(strIntentName)
            objController.fltProbability = fltConfidence

            if fltConfidence > 0.6:
                self.objCurrentUser.clarificationIntentRedirected(objController,strMessage,dictParsedData)
                self.objCurrentUser.current_state = 1
            else:
                self.askClarification(strMessage)   # ask for clarification again.
        else:
            print("Checking sentiment")
            fltPolarity = self.objTextBlobWrapper.analyseSentiment(strMessage)

            if fltPolarity > 0.1:
                objController = self.objIntentMapper.getObjectForIntentId(self.objCurrentIntent.intentId)
                objController.fltProbability = fltPolarity
                self.objCurrentUser.current_state = 1
                self.objCurrentUser.clarificationIntentRedirected(objController,strMessage,dictParsedData)
            else:
                self.askClarification(strMessage)