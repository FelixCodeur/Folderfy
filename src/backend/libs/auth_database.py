import json
import random

def loadDb():
    try:
        with open('db.json', 'r') as f:
            return json.loads(f.read())
    except:
        return {}

def storeDb(db):
    with open('db.json', 'w') as f:
        f.write(json.dumps(db))

db = loadDb()

def generateToken():
    token = ''.join([str(random.randint(0, 9)) for i in range(0, 32)])
    return token

def storeGrant(grant_id):
    token = generateToken()
    db[token] = grant_id
    storeDb(db)

    return token

def getGrant(token):
    if token not in db:
        return None
    grant = db[token]
    return grant