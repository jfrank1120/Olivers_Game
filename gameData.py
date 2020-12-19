from google.cloud import datastore
from game import Game
from main import log

def getClient():
    client = None;
    try:
        client = datastore.Client()
        return client
    except:
        return datastore.Client.from_service_account_json("API_KEY.json")