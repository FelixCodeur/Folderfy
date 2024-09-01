from libs.ai_client import askAI

LABELS = [
    "Work", "Personal", "Finance", "Health", 
    "Travel", "Shopping", "Education", "Social", 
    "Entertainment", "Newsletters", "Projects", 
    "Family", "Events", "Receipts", "Subscriptions", 
    "Promotion", "Not interesting"
]

def sortEmail(subject: str, body: str):
    max_length = 3000
    if len(body) > max_length:
        body = body[-max_length:]
        body = " ... (truncated)\n\n" + body

    prompt = f"Which label should this email be labeled as? Be accurate. Here are the possible labels: {', '.join(LABELS)}. The email is: {subject} {body}"
    res = askAI(prompt)
    most_matching_label = max(LABELS, key=lambda label: res.count(label))

    return most_matching_label