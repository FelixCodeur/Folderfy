from libs.nylas_client import nylas

def getEmails(grant_id: str):
    messages = nylas.messages.list(
        grant_id,
        query_params={
            "limit": 10
        }
    )

    return messages

def sendEmail(grant_id: str, to_name: str, email: str, subject: str, body: str):
    nylas.messages.send(
    grant_id,
    request_body={
        "to": [{ "name": to_name, "email": email }],
        "reply_to": [{ "name": to_name, "email": email }],
        "subject": subject,
        "body": body,
        "attachments": []
    }
)

def _getFolders(grant_id: str):
    folder = nylas.folders.list(
        grant_id
    )
    return folder[0]

def createFolder(grant_id: str, name: str):
    try:
        folder = nylas.folders.create(
            grant_id,
            request_body={
                "name": name,
                "parent": None
                }
        )
        return folder.id

    except:
        folders = _getFolders(grant_id)
        for folder in folders:
            if folder.name.lower() == name.lower():
                return folder.id

def moveEmailToFolder(grant_id: str, message_id: str, folder_id: str):
    nylas.messages.update(
        grant_id,
        message_id,
        request_body={
            "folders": [folder_id]
        }
    )