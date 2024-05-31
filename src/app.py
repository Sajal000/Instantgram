import boto3
import uuid
from flask import Flask, render_template, request

app = Flask(__name__)

S3_BUCKET_NAME = 'S3_BUCKET_NAME'
AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
AWS_REGION = 'AWS_REGION'

STORAGE_URL = "STORAGE_URL"
DYNAMODB_TABLE = 'DYNAMODB_TABLE'

dynamodb = boto3.resource('dynamodb',
                          region_name= AWS_REGION,
                          aws_access_key_id= AWS_ACCESS_KEY_ID,
                          aws_secret_access_key= AWS_SECRET_ACCESS_KEY)


def get_table(image_details):
    client = boto3.resource('dynamodb',
                          region_name= AWS_REGION,
                          aws_access_key_id= AWS_ACCESS_KEY_ID,
                          aws_secret_access_key= AWS_SECRET_ACCESS_KEY)
    table = client.Table(image_details)
    return table

def getBucket():
    s3 = boto3.resource(service_name = 's3', 
                        region_name = AWS_REGION, 
                        aws_access_key_id = AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
    bucket = s3.Bucket(S3_BUCKET_NAME)
    return bucket
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    caption = request.form['caption']

    if file:
        s3_client = boto3.client('s3',
                                 aws_access_key_id=AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                 region_name=AWS_REGION)
        s3_client.upload_fileobj(file, S3_BUCKET_NAME, file.filename)

        image_uuid = str(uuid.uuid4())

        dynamodb_table = dynamodb.Table(DYNAMODB_TABLE)
        dynamodb_table.put_item(
            Item={
                'image_details': image_uuid,
                'caption': caption,
                'image_name': file.filename
            }
        )
        
        image_url = f"{STORAGE_URL}{file.filename}"
        return {'url': image_url, 'caption': caption}, 200
    else:
        return 'Failed to upload photo!', 400


@app.route('/dashboard')
def loadPage():
    dynamodb_table = get_table(DYNAMODB_TABLE)
    response = dynamodb_table.scan()
    items = response['Items']
    for item in items:
        item['url'] = STORAGE_URL + item['image_name']
    return {'results': items } 


if __name__ == '__main__':
    app.run(debug=True)


