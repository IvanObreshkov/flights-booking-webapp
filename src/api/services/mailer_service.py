import os
import boto3
from botocore.exceptions import ClientError

from api.db.models.users_model import Users
from api.utilities.jwt_creation import create_verification_jwt

SENDER = os.getenv("ADMIN_EMAIL")
SUBJECT = "TONI MONTANA"
CHARSET = "UTF-8"
BODY_TEXT = ("This is a test")


class MailerService:
    @classmethod
    def send_verification_email(cls, user: Users) -> None:
        token = create_verification_jwt(user)
        BODY_HTML = f"""<html>
        <head></head>
        <body>
          <h1>Hi welcome to our app, {user.first_name}</h1>
          <p>Please verify your email by clicking
            <a href='http://127.0.0.1:5000/verify?token={token}'>here</a></p>
        </body>
        </html>
                    """
        client = boto3.client('ses', region_name=os.getenv("AWS_REGION"))

        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        user.email,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
