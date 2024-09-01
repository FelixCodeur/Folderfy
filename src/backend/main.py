import www

import dotenv
import os
dotenv.load_dotenv()

keys = [
    'GROQ_API_KEY',
    'RAPID_API_KEY',
    'NYLAS_API_KEY',
    'NYLAS_API_URI',
    'NYLAS_CLIENT_ID'
]

for key in keys:
    if os.environ.get(key) is None:
        raise Exception(f'Environment variable {key} is not set')

www.start()