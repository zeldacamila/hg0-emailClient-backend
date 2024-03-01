import boto3
import os
from botocore.exceptions import ClientError


class MailSender:
    """Encapsulates functions to send emails with Amazon SES."""

    def __init__(self):
        """
        Initializes the MailSender object.
        """
        self.AWS_REGION = os.environ.get('AWS_REGION')
        self.CHARSET = "UTF-8"

        # Retrieve AWS credentials from environment variables
        self.access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        self.ses_client = boto3.client('ses', region_name=self.AWS_REGION,
                                       aws_access_key_id=self.access_key_id,
                                       aws_secret_access_key=self.secret_access_key)

    def send_email(self, sender, recipient, subject, text):
        """
        Sends an email.

        :param source: The source email account.
        :param destination: The destination email account.
        :param subject: The subject of the email.
        :param text: The plain text version of the body of the email.
        :return: The ID of the message, assigned by Amazon SES.
        """

        try:
            response = self.ses_client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': self.CHARSET,
                            'Data': text,
                        },
                    },
                    'Subject': {
                        'Charset': self.CHARSET,
                        'Data': subject,
                    },
                },
                Source=sender,)
            message_id = response["MessageId"]
            print(response)
            print("Sent mail %s from %s to %s.",
                  message_id, sender, recipient)
        except ClientError:
            print("Couldn't send mail from %s to %s.", sender, recipient)
            raise
        else:
            return message_id


if __name__ == "__main__":
    send = MailSender()
    send.send_email(
        sender="test@awesomemailbox.net",
        recipient="vallejocas1020@gmail.com",
        subject="test from python",
        text="this is a test from python"
    )
