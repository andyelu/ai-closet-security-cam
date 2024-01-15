from datetime import datetime
import requests
from dotenv import load_dotenv
from google.cloud import vision
import os
from PIL import Image
from io import BytesIO
from api.models import Event
import boto3
from botocore.exceptions import NoCredentialsError
from email.message import EmailMessage
import ssl
import smtplib

load_dotenv()
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def get_frame():
    # get the current frame displayed on the esp-32 cam web server
    response = requests.get("http://192.168.1.39/saved-photo")

    if response.status_code == 200:
        image_data = response.content
        if analyze_image(image_data):
            bucket_name = "esp32-photos"
            image_url = upload_to_s3(image_data, bucket_name)

            if image_url:
                # Send notification and URL to user
                send_notification(image_url)
                # Save the URL to the database
                event = Event(image_data=image_url)
                event.save()
                print("Image URL saved to database")
            else:
                print("Failed to upload to S3.")
        else:
            print("No person detected, image not saved.")
    else:
        print("Failed to retrieve the image. Status code:", response.status_code)

def analyze_image(image_data):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_data)

    objects = client.object_localization(image=image).localized_object_annotations
    print(f"Number of objects found: {len(objects)}")

    for object_ in objects:
        if object_.name == "Person":
            print('Person detected')
            return True  # Return True if a person is detected

    return False  # Return False if no person is detected

def upload_to_s3(image_data, bucket_name):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    s3_file_name = f"image_{timestamp}.jpg"
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket=bucket_name, Key=s3_file_name, Body=image_data)
        print("Upload Successful")
        return f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name}"
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None
    
def send_notification(s3_url):
    email_sender = os.getenv('EMAIL_SENDER')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_receiver = os.getenv('EMAIL_RECEIVER')

    subject = "Person detected by your ESP32 CAM"
    body = f"Person detected: {s3_url}"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    print(f'Sent email to {email_receiver}')