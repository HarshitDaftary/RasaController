from User.User import User
import os
import io
import json
import random
import sys
import os.path

class WebUser(User):
    strSessionId = ""
    
    def updateUserMetadata(self):
        pass            