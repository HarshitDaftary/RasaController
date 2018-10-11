import io
import json
from snips_nlu import load_resources, SnipsNLUEngine
import os
import sys

script_dir = os.path.dirname(__file__)

class SnipsWrapper(object):

	nlu_engine = SnipsNLUEngine()

	def train(self,strFileName):
		path = os.path.join(script_dir, strFileName)
		with io.open(path) as f:
			sample_dataset = json.load(f)
		self.nlu_engine.fit(sample_dataset)
		self.nlu_engine.persist(script_dir + "/model")


	def __init__(self):

		print('initializing Snips NLU Begin')
		load_resources(u"en")
		#self.train("sample_dataset.json")
		print('initializing Snips NLU Complete')


	def parseFromFile(self,strInput, strEngineFilePath):
		
		loaded_engine = SnipsNLUEngine.from_path(script_dir + "/model")

		print("current python version ",sys.version_info[0])

		if sys.version_info[0] < 3:
			parsing = loaded_engine.parse(unicode(strInput,"utf-8"))
		else:
			parsing = loaded_engine.parse(strInput)

		print(json.dumps(parsing, indent=2))

		loaded_json = json.loads(json.dumps(parsing, indent=2))
		return loaded_json

	def parse(self,strInput):
		return self.parseFromFile(strInput,"")
		
		
		
