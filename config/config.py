
from dotenv import load_dotenv
import os

dotenv_path = os.getenv("ENV_FILE_PATH")
load_dotenv(dotenv_path=dotenv_path)

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

configuration = {
    'AWS_ACCESS_KEY': AWS_ACCESS_KEY,
    'AWS_SECRET_KEY': AWS_SECRET_KEY
}
print(f"API Key: {AWS_ACCESS_KEY}")
print(f"AWS_SECRET_KEY URL: {AWS_SECRET_KEY}")