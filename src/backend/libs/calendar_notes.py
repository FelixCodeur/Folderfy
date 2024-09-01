from libs.ai_client import askAI
import time

def makeNote(event):
    title = event["title"]
    duration = (event["end_time"] - event["start_time"]) / 60 / 60

    prompt = f"Create a short note for a event on Google Calendar titled '{title}' and lasts {duration} hours. In case it's something boring, like work, make it funny so it makes you feel better. Dont't include any placeholders. Don't write any other text except the note that should be displayed."

    return askAI(prompt)