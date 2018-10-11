import random
import sys
import os
import io
import json
import random

script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir, "NLP/SnipsNLUWrapper/sample_dataset.json")

with io.open(path) as f:
    sample_dataset = json.load(f)

class IntentController(object):

    intentId = ""
    followupIntentId = ""
    arrDetectedSlots = []
    arrRequiredSlots = []
    arrMissingSlots = []
    arrParentControllers = []
    fltProbability = 0.0
    
    objCurrentMissingSlot = ""
    objCurrentUser = None
    

    def clearInternalStorage(self):
        del self.arrDetectedSlots[:]
        del self.arrRequiredSlots[:]
        del self.arrMissingSlots[:]
        del self.arrParentControllers[:]
        self.arrDetectedSlots = []
        self.arrRequiredSlots = []
        self.arrMissingSlots = []
        self.arrParentControllers = []
        self.objCurrentMissingSlot = ""
        self.followupIntentId = ""


    def addToDetectedSlot(self,objSlot):
        self.arrDetectedSlots.append(objSlot)

    def parseDetectedSlots(self,arrTmpDetectedSlots,arrTmpRequiredSlots):
        del self.arrDetectedSlots[:]

        if len(arrTmpDetectedSlots) > 0 and len(arrTmpRequiredSlots) > 0:
            for objDetectedSlot in arrTmpDetectedSlots:
                for objRequiredSlot in arrTmpRequiredSlots:
                    if objDetectedSlot["slotName"]==objRequiredSlot["slot"]:
                        objFinalSlot = objRequiredSlot
                        objFinalSlot["value"] = objDetectedSlot["rawValue"]
                        self.addToDetectedSlot(objFinalSlot)
                
            

    def getMissingSlots(self,arrTmpDetectedSlots,arrTmpRequiredSlots):
        del self.arrMissingSlots[:]

        if len(arrTmpRequiredSlots) > 0:
            for objRequiredSlot in arrTmpRequiredSlots:
                slotFound = False
                if arrTmpDetectedSlots != None and len(arrTmpDetectedSlots) > 0:
                    for objDetectedSlot in  arrTmpDetectedSlots:
                        if objDetectedSlot["slotName"]==objRequiredSlot["slot"]:
                            slotFound = True
                if slotFound == False:
                    self.arrMissingSlots.append(objRequiredSlot)

            
        return self.arrMissingSlots

    def __init__(self):
        print('--initialisation Super IntentController')

    def returnIntentName(self):
        return self.intentId

    def intentIdentifier(self,string):
        print('--Parsing method')

    def intentDetected(self,inputStatement):
        self.clearInternalStorage()
        print("after cleaning --> arrMissingSlots",len(self.arrMissingSlots))
        print("after cleaning --> arrRequiredSlots",len(self.arrRequiredSlots))
        print("--Intent detected method")

    def requiredSlotsForIntent(self,slotList):
        self.arrRequiredSlots = slotList
        return slotList

    def detectedSlots(self,slotList):
        print("--Slots detected",slotList)

    def shouldAskForSlot(self,slot):
        print("--Should ask for slot: ",slot["slot"])
        return True

    def shouldWriteSlot(self,slot,value):
        return True

    def didWriteToSlot(self,objMissingSlot):
        print("--Wrote to slot")

    def shouldOverwriteSlot(self,detectedSlot, askedSlot,value):
        return False

    def didSetIntent(self,intent):
        print("--Intent set")

    def intentFulfilled(self):
        print("My intent id is ->",self.intentId)
        if 'completion_messages' in sample_dataset['intents'][self.intentId]:
            arrCompletionMessages = sample_dataset['intents'][self.intentId]['completion_messages']
            intIndex = random.randint(0,len(arrCompletionMessages)-1)
            strMessage = arrCompletionMessages[intIndex]
            self.objCurrentUser.messageFromIntent(self,strMessage)
        print("--Intent fulfilled")

    def redirectingToFollowupIntent(self,objTargetIntentController):
        
        objTargetIntentController.arrParentControllers.append(self)
        print("--Followup intent redirection")

    def fillSlots(self,objSnipsWrapper):

        for objMissingSlot in self.arrMissingSlots:
            if 'value' in objMissingSlot:
                print("-- Wow that already existed --",objMissingSlot["slot"])
                print("Value --> ",objMissingSlot["value"])
            else:
                arrTmpValidations = objMissingSlot["validations"]
                intIndex = random.randint(0,len(arrTmpValidations)-1)
                objMissingSlot["validation_msg"] = arrTmpValidations[intIndex]
                self.objCurrentMissingSlot = objMissingSlot
                self.objCurrentUser.messageFromIntent(self,objMissingSlot["validation_msg"])
                print("setting Director Current state as 2")
                self.objCurrentUser.current_state = 2
                break

        if len(self.arrDetectedSlots) == len(self.arrRequiredSlots):
            self.objCurrentUser.intentFillingCompleted(self)
        else:
            print("Still there is a required slot missing")

    def userProvidedSlotInput(self,strInput,objSnipsWrapper):

        slot_value = strInput
        dictParsedData = objSnipsWrapper.parse(slot_value)
        arrTmpDetectedSlot = dictParsedData["slots"]
        objMissingSlot = self.objCurrentMissingSlot
        if arrTmpDetectedSlot != None and len(arrTmpDetectedSlot)>0:
            print("Detected slots is not None")
            for objProvidedSlot in arrTmpDetectedSlot:
                strProvidedValue = ""
                if objProvidedSlot["value"]["kind"] == "TimeInterval":
                    strProvidedValue = objProvidedSlot["value"]["from"] + "T" + objProvidedSlot["value"]["to"]
                else:
                    strProvidedValue = objProvidedSlot["value"]["value"]

                # Check if provided value exactly belongs to the requested slot with datatype.
                if objProvidedSlot["entity"]==objMissingSlot["entity"] and objMissingSlot["slot"]==objProvidedSlot["slotName"]:
                    if self.shouldWriteSlot(strProvidedValue,objMissingSlot["slot"]) == True:
                        objMissingSlot["value"]=strProvidedValue
                        self.didWriteToSlot(objMissingSlot)
                        self.addToDetectedSlot(objMissingSlot)
                        self.objCurrentUser.intentFillingCompleted(self)

                # Check if NLP by mistake filled in wrong slot but value was for requested slot
                elif objProvidedSlot["entity"]==objMissingSlot["entity"] and objMissingSlot["slot"]!=objProvidedSlot["slotName"]:
                    if self.shouldWriteSlot(strProvidedValue,objMissingSlot["slot"]) == True:
                        objMissingSlot["value"]=strProvidedValue
                        self.didWriteToSlot(objMissingSlot)
                        self.addToDetectedSlot(objMissingSlot)
                        self.objCurrentUser.intentFillingCompleted(self)
                                
                    else:  
                        for objTmpDetectedSlots in self.arrDetectedSlots:
                            # Go with the suggestion of NLP, slot is already filled so checking if we can overwrite.
                            if objTmpDetectedSlots["slot"]==objProvidedSlot["slotName"]:
                                if self.shouldOverwriteSlot(objTmpDetectedSlots["slot"],objMissingSlot["slot"],strProvidedValue) == True:
                                    objTmpDetectedSlots["value"]=strProvidedValue
                                    self.didWriteToSlot(objMissingSlot)
                                    self.objCurrentUser.intentFillingCompleted(self)

                else:
                    # Nothing matches with requested slot. So user provided data of another missing slot.
                    for objTmpMissingSlot in self.arrMissingSlots:
                        if objTmpMissingSlot["slot"]==objProvidedSlot["slotName"]:
                            if self.shouldWriteSlot(strProvidedValue,objTmpMissingSlot["slot"]) == True:
                                objTmpMissingSlot["value"]=strProvidedValue
                                self.didWriteToSlot(objTmpMissingSlot)
                                self.addToDetectedSlot(objTmpMissingSlot)
                                self.objCurrentUser.intentFillingCompleted(self)

        else:
            #NLP could not detect anything.
            print("Try again")
            self.objCurrentUser.messageFromIntent(self,"Sorry I could not get. Please try again.")
            return