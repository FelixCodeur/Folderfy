import dotenv
dotenv.load_dotenv()

import requests
import os
from libs.ai_client import askAI

url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"

def translate(email_content, target_language):
    lang_content = email_content[-300:]
    email_language = askAI(f"What is the language of the following text? JUST answer by the language 2 letter code, as 'en' (for english) or 'es' (for espagnol). NEVER say something else than that. Here is the text: {lang_content}")
    if email_language == target_language:
        return email_content
    
    payload = {
        "q": email_content,
        "source": email_language,
        "target": target_language
    }
    headers = {
        "x-rapidapi-key": os.environ.get('RAPID_API_KEY'),
        "x-rapidapi-host": "deep-translate1.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    translation = response.json()["data"]["translations"]["translatedText"]

    return translation