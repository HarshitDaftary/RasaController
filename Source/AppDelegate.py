from NLP.SnipsNLUWrapper.SnipsWrapper import SnipsWrapper
from NLP.RasaNLUWrapper.RasaWrapper import RasaWrapper
from NLP.TextBlobNLPWrapper.TextBlobWrapper import TextBlobWrapper
from NLP.DucklingNLPWrapper.DucklingNLPWrapper import DucklingNLPWrapper
from Medium.WebMedium import WebMedium

import os
import io
import json
import random
import sys

class AppDelegate(object):
    
    current_mode = 1
    objSnipsWrapper = ""
    objRasaWrapper = ""
    objDucklingWrapper = ""
    strCurrentUserInput = ""
    objCurrentIntent = ""

    objWebMedium = WebMedium()

    def __init__(self):
        print('initialisation of AppDelegate')  

    def startNLUServers(self):
        self.objSnipsWrapper = SnipsWrapper()
        #self.objRasaWrapper = RasaWrapper()
        #self.objTextBlobWrapper = TextBlobWrapper()
        #self.objDucklingWrapper = DucklingNLPWrapper()  

        
    def processWebMessage(self, dictIncomingmessage):
        self.objWebMedium.objSnipsWrapper = self.objSnipsWrapper
        self.objWebMedium.processIncomingMessage(dictIncomingmessage)
        return self.objWebMedium.getPendingMessages(dictIncomingmessage)