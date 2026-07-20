from django.conf.urls import url
import json


def getPickleData(pickled):
    '''
    Return deserialized data
    '''
    return json.loads(pickled)