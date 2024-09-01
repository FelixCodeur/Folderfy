import json

def _getReadEmails():
    emails = {}
    try:
        with open('emails.json', 'r') as f:
            emails = json.loads(f.read())
    except:
        pass
    return emails

emails = _getReadEmails()

def getReadEmails(userId):
    if userId not in emails:
        emails[userId] = []
    return emails[userId]

def addToReadEmails(userid, emailId):
    if userid not in emails:
        emails[userid] = []
    emails[userid].append(emailId)
    with open('emails.json', 'w') as f:
        f.write(json.dumps(emails))