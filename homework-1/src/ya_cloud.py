from dotenv import load_dotenv
import os
from boto3.session import Session


load_dotenv()

AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']
REGION=os.environ['REGION']
BUCKET_NAME=os.environ['BUCKET_NAME']

session = Session()

s3 = session.resource(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name=REGION,
)

bucket = s3.Bucket(BUCKET_NAME)