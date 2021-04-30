import json
import random
import math
import boto3
from botocore.client import Config
import time
import os

ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
ACCESS_SECRET_KEY = os.environ['ACCESS_SECRET_KEY']
BUCKET_NAME = 'kaggle-top20-predictor'


def to_s3(data):
    """
    Persist the input_data and calculated score to S3
    """
    dt = time.strftime('%Y-%m-%d_%H-%M-%S')
    # add the created at data to json
    final_data = {'created_at': dt,
                  'data': data}

    # Set filename
    FILE_NAME = dt + "kaggle-survey-response-" + str(random.randrange(1, 100)) + ".json"

    # dumps to str
    final_data = json.dumps(final_data, indent=4, ensure_ascii=False)

    # S3 Connect
    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4'))

    # Uploaded File
    s3.Bucket(BUCKET_NAME).put_object(Key=FILE_NAME, Body=final_data)
