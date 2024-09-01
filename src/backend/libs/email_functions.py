from libs.email_database import addToReadEmails, getReadEmails
from libs.email_client import getEmails, moveEmailToFolder, createFolder, _getFolders
from libs.email_sorter import sortEmail

folders = {}

def getFolderById(grant_id, folder_id):

    if grant_id not in folders:
        _folders = _getFolders(grant_id)
        folders[grant_id] = _folders

    _folders = folders[grant_id]

    if grant_id not in folders:
        _folders = _getFolders(grant_id)
        folders[grant_id] = _folders
    
    _folders = folders[grant_id]
    for folder in _folders:
        if folder.id == folder_id:
            return folder.name

def _getAllEmails(grant_id):
    allEmails = getEmails(grant_id)[0]
    readEmails = getReadEmails(grant_id)

    unreadEmailsIds = []
    for email in allEmails:
        if email.id not in readEmails:
            unreadEmailsIds.append(email.id)
            addToReadEmails(grant_id, email.id)

    mails_all = []
    for mail in allEmails:
        foldersIds = mail.folders
        folderNames = []
        for folder in foldersIds:
            folderNames.append(getFolderById(grant_id, folder))
        data = {
            "id": mail.id,
            "subject": mail.subject,
            "body": mail.body,
            "from": mail.from_[0],
            "unread": unreadEmailsIds.__contains__(mail.id),
            "folders": folderNames,
            "snippet": mail.snippet
        }

        mails_all.append(data)

    return mails_all

def getAllEmails(grant_id):
    emails = _getAllEmails(grant_id)
    result = []

    for email in emails:
        email_id = email["id"]
        subject = email["subject"]
        body = email["body"]
        from_email = email["from"]
        unread = email["unread"]
        folders = email["folders"]
        snippet = email["snippet"]

        if unread:
            print('putting email in folder...')
            folderName = sortEmail(subject, body) 
            folder_id = createFolder(grant_id, folderName)
            moveEmailToFolder(grant_id, email_id, folder_id)
            folders.append(folderName)
            
        result.append({
            "id": email_id,
            "subject": subject,
            "body": body,
            "from": from_email,
            "unread": unread,
            "folders": folders,
            "snippet": snippet
        })

    return result