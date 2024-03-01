import boto3
import os
from botocore.exceptions import ClientError


class MailSender:
    """Encapsulates functions to send emails with Amazon SES."""

    def __init__(self):
        """
        Initializes the MailSender object.
        """

        self.AWS_REGION = "us-east-2"
        self.CHARSET = "UTF-8"

        # Retrieve AWS credentials from environment variables
        self.access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        self.ses_client = boto3.client('ses', region_name=self.AWS_REGION,
                                       aws_access_key_id=self.access_key_id,
                                       aws_secret_access_key=self.secret_access_key)

    def send_email(self, source, destination, subject, text):
        """
        Sends an email.

        :param source: The source email account.
        :param destination: The destination email account.
        :param subject: The subject of the email.
        :param text: The plain text version of the body of the email.
        :return: The ID of the message, assigned by Amazon SES.
        """
        send_args = {
            "Source": source,
            "Destination": destination.to_service_format(),
            "Message": {
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": text}},
            },
        }

        try:
            response = self.ses_client.send_email(**send_args)
            message_id = response["MessageId"]
            print("Sent mail %s from %s to %s.",
                  message_id, source, destination.tos)
        except ClientError:
            print("Couldn't send mail from %s to %s.", source, destination.tos)
            raise
        else:
            return message_id
