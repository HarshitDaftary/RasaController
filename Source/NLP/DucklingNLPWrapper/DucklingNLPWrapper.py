import io
import sys
from duckling.duckling import Duckling

class DucklingNLPWrapper(object):

    objDuckling = Duckling()

    def __init__(self):
        print("Duckling init command")
        self.objDuckling.load()
    
    def parse(self,strInput):
        
        if sys.version_info[0] < 3:
            print(self.objDuckling.parse(unicode(strInput,"utf-8")))
        else:
            print(self.objDuckling.parse(strInput))
