import io
import json
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import os
import sys
script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir, "train.json")

with open(path, 'r') as fp:
     cl = NaiveBayesClassifier(fp, format="json")

class TextBlobWrapper(object):

    def __init__(self):
        print("init command")
    
    def parse(self,strInput):
        prob = ""

        if sys.version_info[0] < 3:
            prob = cl.classify(unicode(strInput,"utf-8"))
        else:
            prob = cl.classify(strInput)

        print(prob)

    def analyseSentiment(self,strInput):
        parsedData = TextBlob("Textblob is amazingly simple to use. What great fun!")
        print("Sentiment analysis says ->",parsedData.sentiment)
        return parsedData.sentiment.polarity

