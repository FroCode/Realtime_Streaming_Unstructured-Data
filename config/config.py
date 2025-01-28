
from dotenv import load_dotenv
import os

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

configuration = {
    'AWS_ACCESS_KEY': AWS_ACCESS_KEY,
    'AWS_SECRET_KEY': AWS_SECRET_KEY
}