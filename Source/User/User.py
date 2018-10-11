from NLP.SnipsNLUWrapper.SnipsWrapper import SnipsWrapper
from IntentController import IntentController
from IntentMapper import IntentMapper
from ClarificationIntent import ClarificationIntentController

import os
import io
import json
import random
import sys
import os.path


script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir, "../slots.json")

slot_database = None
with io.open(path) as f:
    slot_dataset = json.load(f)
    slot_database = slot_dataset.copy()

import enum
 
# creating enumerations using class
class ListeningState(enum.Enum):
    intentRead = 1
    slotRead = 2
    clarificationRead = 3

class User(object):

    objIntentMapper = IntentMapper()
    strCurrentUserInput = ""
    objCurrentIntent = ""
    objSnipsWrapper = None
   
    current_state = 1
    objClaraificationIntent = ""
    arrIntentControllers = []
    objCurrentMedium = None

    def __init__(self):
        print("Initialize")

    def updateUserName(self):
        pass

    def userSentMessage(self, strUserInput):

        print("User sent message ",strUserInput)
        print("User received input with state ",self.current_state)

        if self.current_state == 1:
            self.parseUsingSnips(strUserInput)
        elif self.current_state == 2:
            self.forwardToCurrentIntent(strUserInput)
        elif self.current_state == 3:
            self.objClaraificationIntent.userAnswered(strUserInput)
            print("Forwarded input to clarification intent")
            print("Curren state is ",self.current_state)

    def isRelatedWithFollowupIntent(self, strUserInput):

        isFollowUpIntent = False

        if self.arrIntentControllers != None and len(self.arrIntentControllers) > 0:
            objPreviousIntentController = self.arrIntentControllers[-1]
            strIntentName = objPreviousIntentController.intentId
            #strEngineFilePath = os.path.join(script_dir, "../NLP/SnipsNLUWrapper/" + strIntentName + "_engine" + ".json")
            strEngineFilePath = os.path.join(script_dir, "../NLP/SnipsNLUWrapper/" + "sample.json")

            if os.path.exists(strEngineFilePath) == True:
                dictParsedData = self.objSnipsWrapper.parseFromFile(strUserInput,strEngineFilePath)

                if dictParsedData["intent"] != None:
                    strIntentName = dictParsedData["intent"]["intentName"]
                    fltConfidence = dictParsedData["intent"]["probability"]

                    if fltConfidence > 0.6:
                        if dictParsedData["slots"] != None:
                            arrDetectedSlots = dictParsedData["slots"]

                        isFollowUpIntent = True
                        strInput = dictParsedData["input"]
                        objController = None
                        objController = self.objIntentMapper.getObjectForIntentId(strIntentName)
                        self.arrIntentControllers.append(objController)
                        objController.fltProbability = fltConfidence
                        self.objCurrentIntent = objController
                        objController.objCurrentUser = self
                        objController.intentDetected(strInput)
                        self.completeIntent(objController,dictParsedData)
        
        return isFollowUpIntent


    def parseUsingSnips(self, strUserInput):

        #Check if this input belongs to previous intent's follow up intent.
        if self.isRelatedWithFollowupIntent(strUserInput) == True:
            print("Went in followup intent")
        else:
        #if self.current_state == 1:
            dictParsedData = self.objSnipsWrapper.parseFromFile(strUserInput,"")
            
            if dictParsedData["intent"] != None:
                
                strIntentName = dictParsedData["intent"]["intentName"]
                fltConfidence = dictParsedData["intent"]["probability"]

                if fltConfidence > 0.6:
                    if dictParsedData["slots"] != None:
                        arrDetectedSlots = dictParsedData["slots"]

                    strInput = dictParsedData["input"]
                    objController = None
                    objController = self.objIntentMapper.getObjectForIntentId(strIntentName)
                    self.arrIntentControllers.append(objController)
                    objController.fltProbability = fltConfidence
                    self.objCurrentIntent = objController
                    objController.objCurrentUser = self
                    objController.intentDetected(strInput)
                    self.completeIntent(objController,dictParsedData)
                else:   #Probability is less so we need to clarify with user.
                    print("sending to clarification intent")
                    self.objClaraificationIntent = ClarificationIntentController()
                    self.objClaraificationIntent.objCurrentIntent = self.objIntentMapper.getObjectForIntentId(strIntentName)
                    self.objClaraificationIntent.objCurrentIntent.fltProbability = fltConfidence
                    self.objCurrentIntent = self.objClaraificationIntent
                    self.objClaraificationIntent.objCurrentUser = self
                    self.objClaraificationIntent.objSnipsWrapper = self.objSnipsWrapper
                    self.objClaraificationIntent.askClarification(strUserInput)

            else:
                print("Call fall back intent")
        #else:
        #    self.objCurrentIntent.userProvidedSlotInput(strUserInput,self.objSnipsWrapper)

    def forwardToCurrentIntent(self,strUserInput):
        self.objCurrentIntent.userProvidedSlotInput(strUserInput,self.objSnipsWrapper)

    def completeIntent(self,objController,dictParsedData):

        self.current_state = 1
        print("Before for loop")

        hasRequriedSlots = False

        with io.open(path) as f:
            slot_dataset = json.load(f)
            slot_database = slot_dataset.copy()
        
        dictRootMapping = slot_database.copy()

        for objTmpMapping in dictRootMapping["mapping"]:
            
            if objTmpMapping["intent"] == objController.returnIntentName():
                hasRequriedSlots = True
                arrRequiredSlots = objTmpMapping["slots"]
                print("Mapping is ->",objTmpMapping)
                print("Read slots as ->",arrRequiredSlots)
                
                arrRequiredSlots = objController.requiredSlotsForIntent(arrRequiredSlots.copy())

                print("For loop")
                print("Required Slosts ->",arrRequiredSlots)
                if len(arrRequiredSlots)==0 or arrRequiredSlots == []:
                    print("Required slosts are zero")
                    self.intentFillingCompleted(self.objCurrentIntent)
                    return

                if dictParsedData != None and 'slots' in dictParsedData and dictParsedData["slots"] != None:
                    arrDetectedSlots = dictParsedData["slots"]
                    objController.parseDetectedSlots(arrDetectedSlots,arrRequiredSlots)
                    objController.detectedSlots(objController.arrDetectedSlots)

                arrFinalMissingSlots = objController.getMissingSlots(None,arrRequiredSlots)
                
                if len(objController.arrDetectedSlots) != len(objController.arrRequiredSlots):
                    objController.fillSlots(self.objSnipsWrapper)
                else:
                    print("we don't have missing slots")
                    if len(objController.arrDetectedSlots) == len(objController.arrRequiredSlots):
                        self.intentFillingCompleted(objController)
        
        if hasRequriedSlots == False:
            objController.intentFulfilled()
            self.current_state = 1
                # Let's try to fill the missing slot with other Wrappers.
                #self.objDucklingWrapper.parse(self.strCurrentUserInput)

    def intentFillingCompleted(self,objIntentController):

        print("Intent filling completed")
        objController = objIntentController
        mapping = ""
        
        self.current_state = 1

        with io.open(path) as f:
            slot_dataset = json.load(f)
            slot_database = slot_dataset.copy()

        dictRootMapping =  slot_database.copy()

        for objTmpMapping in dictRootMapping["mapping"]:
            if objTmpMapping["intent"] == objController.returnIntentName():
                mapping = objTmpMapping

        if len(objController.arrRequiredSlots) == 0:
            objController.intentFulfilled()

        elif len(objController.arrDetectedSlots) != len(objController.arrRequiredSlots):
            objController.fillSlots(self.objSnipsWrapper)
                
        elif len(objController.arrDetectedSlots) == len(objController.arrRequiredSlots):
            objController.intentFulfilled()
    
    def clarificationIntentRedirected(self,objIntentController,strInput,dictParsedData):
        self.objCurrentIntent = objIntentController
        self.objCurrentIntent.objCurrentUser = self
        self.objCurrentIntent.intentDetected(strInput)
        self.completeIntent(self.objCurrentIntent,dictParsedData)
        self.objClaraificationIntent = None

    def messageFromIntent(self,objIntentController,strMessage):
        self.objCurrentMedium.sendMessageBack(self,strMessage)
        pass