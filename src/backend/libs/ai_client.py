import dotenv
dotenv.load_dotenv()

from groq import Groq
import os

api_key = os.environ.get('GROQ_API_KEY')
client = Groq(api_key=api_key)

def askAI(prompt: str):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Always answer short and concise questions. Be professional."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )


    response = completion.choices[0].message.content
    return response

def askRaw(messages: list):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    response = completion.choices[0].message.content
    return response