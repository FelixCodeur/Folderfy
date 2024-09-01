from libs.email_functions import getAllEmails 
from libs.ai_client import askRaw
from libs.calendar_client import getAllEvents
from datetime import datetime
from libs.ai_client import askAI

convos = {}

def timestamp_to_text(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def initConvo(grant_id):
    emails = getAllEmails(grant_id)
    emails = emails[:7]
    emails = [{"from": email["from"], "subject": email["subject"], "folders": email["folders"], "unread": email["unread"], "body": email["body"][:100]} for email in emails]

    events = getAllEvents(grant_id)
    events = events[:7]
    events = [{"title": event["title"][:25], "start": timestamp_to_text(event["when"].start_time), "end": timestamp_to_text(event["when"].end_time)} for event in events]

    systemPrompt = f"You are an AI assistant that helps people with their email and calendar. You will be given an prompt and you should answer. You only have access to the first 7 emails and the first 7 events. Do what the user ask, you can summarize emails. Since you only have access to email body, try extracting the email text from it. Never talk too much. Here are the events: \"{events}\". Here are the emails: \"{emails}\""
    convos[grant_id] = [
        {
            "role": "system",
            "content": systemPrompt
        }
    ]
    

def ask(grant_id, prompt):
    if grant_id not in convos:
        return "Error: No conversation found"
    
    convos[grant_id].append({
        "role": "user",
        "content": prompt
    })
    
    response = askRaw(convos[grant_id])

    convos[grant_id].append({
        "role": "assistant",
        "content": response
    })

    return response