from dotenv import load_dotenv
load_dotenv()

import os
from nylas import Client

nylas = Client(
    os.environ.get('NYLAS_API_KEY'),
    os.environ.get('NYLAS_API_URI')
)