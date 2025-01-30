from dotenv import load_dotenv
import os
import json

dotenv_path = ("aws.env")
load_dotenv(dotenv_path=dotenv_path)

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

#s3 bucket config

def get_s3_pyspark_url():
    # Load the JSON data from the file
    with open('terraform_outputs.json') as f:
        outputs = json.load(f)
    # Access the s3_pyspark_url value
    s3_url = outputs['s3_pyspark_url']['value']
    return s3_url

configuration = {
    'AWS_ACCESS_KEY': AWS_ACCESS_KEY,
    'AWS_SECRET_KEY': AWS_SECRET_KEY,
    's3_pyspark_url': get_s3_pyspark_url()
}
