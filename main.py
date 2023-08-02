import aiogram
import os
from dotenv import load_dotenv

load_dotenv()

print(f'Your token is: {os.getenv("TOKEN")}')
