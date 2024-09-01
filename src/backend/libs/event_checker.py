from libs.ai_client import askAI
import time

def _parseDateFromString(date: str):
    newDate = ""

    for char in date:
        if char in "0123456789-_:":
            newDate += char

    for _ in range(4):
        if (newDate[0] in "-_:"):
            newDate = newDate[1:]
    
    newDate = time.strptime(newDate, "%Y-%m-%d_%H:%M")
    timestamp = time.mktime(newDate)
    
    return timestamp

def shouldAddEvent(subject: str, body: str):
    max_length = 3000
    if len(body) > max_length:
        body = body[-max_length:]
        body = " ... (truncated)\n\n" + body
    prompt = f"Does this email contain something that needs to be added to the calendar? This is the email: {subject} {body}. If it contains something that needs to be added to the calendar, respond with 'Yes' plus the details. If it doesn't contain anything that needs to be added to the calendar, respond with 'No'."
    res = askAI(prompt)
    print(res)
    yes_index = res.lower().find("yes")
    no_index = res.lower().find("no")

    if yes_index == -1:
        yes_index = 1000

    if no_index == -1:
        no_index = 1000

    is_event = yes_index < no_index

    if is_event == False:
        print("Not adding event")
        return { "shouldAdd": False }

    title = askAI(f"Create a title for an event based on this: {res}. Don't include the date. Keep it as short as possible.")
    startDate = askAI(f"Create a start date for an event based on this: {res}. The format should be YYYY-MM-DD_HH:MM. The date should be in the future or today. The current date is {time.strftime('%A, %Y-%m-%d')}. Keep it as short as possible.")
    endDate = askAI(f"Create an end date for an event based on this: {res}. The format should be YYYY-MM-DD_HH:MM. The date should be in the future or today. The current date is {time.strftime('%A, %Y-%m-%d')}. Keep it as short as possible. Make sure the end date is after the start date.")

    print(title)
    print(_parseDateFromString(startDate))
    print(_parseDateFromString(endDate))

    return { "shouldAdd": True, "title": title, "startDate": int(_parseDateFromString(startDate)), "endDate": int(_parseDateFromString(endDate)) }