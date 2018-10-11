import copy

from Controllers.IntentController import IntentController

class IntentMapper(object):

    arrIntentsList = []

    def __init__(self):
        # objGreetingIntentController = GreetingIntentController()
        # objGreetingIntentController.intentId = "greetings"
        # self.arrIntentsList.append(objGreetingIntentController)
        pass


    def getObjectForIntentId(self,strIntentId):
        print("Get Object for intent id function")
        for controller in self.arrIntentsList:
            print("Checking intent with name ",controller.intentId)
            if controller.intentId == strIntentId:
                controller.clearInternalStorage()
                return copy.copy(controller)

        objIntentController = IntentController()
        objIntentController.intentId = strIntentId
        #self.arrIntentsList.append(objIntentController)
        return copy.copy(objIntentController)