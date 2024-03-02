from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import Email
from user_api.models import User
from .serializers import EmailSerializer


class TestEmailList(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_get_all_emails(self):
        """
        Test that we can retrieve all emails
        """

        # Create some test emails
        email1 = Email.objects.create(
            subject='Test Email 1', sender=self.user, recipient=self.user, status=True)
        email2 = Email.objects.create(
            subject='Test Email 2', sender=self.user, recipient=self.user, status=False)

        # Make a GET request to retrieve all emails
        response = self.client.get('/emails/list/all/')

        # Check if the request was successful (HTTP 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data matches the expected serialized data
        expected_data = EmailSerializer([email1, email2], many=True).data
        self.assertEqual(response.data["data"], expected_data)

    def test_create_new_email(self):
        """
        Test that we can create a new email
        """

        User.objects.create_user(
            username='testuser2', email='test2@example.com', password='testpassword2')

        # Create a new email
        new_email = {
            "subject": "Test Email 3",
            "body": "This is a test email",
            "recipient_email": "test@example.com",
            "sender_email": "test2@example.com",
            "priority": "low"
        }

        # Make a POST request to create a new email
        response = self.client.post('/emails/list/create/', new_email)

        # Check if the request was successful (HTTP 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the email was created successfully
        email = Email.objects.get(subject="Test Email 3")
        self.assertEqual(email.subject, new_email["subject"])

    def test_get_emails_by_sender(self):
        """
        Test that we can retrieve emails by sender
        """

        testUser = User.objects.create_user(
            username='testuser2', email='test2@example.com', password='testpassword2')

        # Create some test emails with specific sender email addresses
        email1 = Email.objects.create(
            subject='Test Email 1', sender=self.user, recipient=testUser, status=True)
        email2 = Email.objects.create(
            subject='Test Email 2', sender=self.user, recipient=testUser, status=False)

        # Make a GET request to retrieve emails by sender
        sender_email = 'test@example.com'
        response = self.client.get(f'/emails/list/sender/{sender_email}/')

        # Check if the request was successful (HTTP 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data matches the expected serialized data
        expected_emails = Email.objects.filter(sender__email=sender_email)
        expected_data = EmailSerializer(expected_emails, many=True).data
        self.assertEqual(response.data['data'], expected_data)

    def test_get_emails_by_status(self):
        """
        Test that we can retrieve emails by status
        """

        # Create some test emails with different statuses
        email1 = Email.objects.create(
            subject='Test Email 1', sender=self.user, recipient=self.user, status=True)
        email2 = Email.objects.create(
            subject='Test Email 2', sender=self.user, recipient=self.user, status=False)

        # Make a GET request to retrieve emails by status
        response = self.client.get('/emails/list/status/true/')

        # Check if the request was successful (HTTP 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data matches the expected serialized data
        expected_emails = Email.objects.filter(status=True)
        expected_data = EmailSerializer(expected_emails, many=True).data
        self.assertEqual(response.data['data'], expected_data)

    def test_update_email(self):
        """
        Test that we can update an email
        """

        # Create a test email
        email = Email.objects.create(
            subject='Test Email', sender=self.user, recipient=self.user, status=True)

        # Define updated email data
        updated_data = {
            "sender_email": "admin@admin.com",
            "recipient_email": "admin@admin.com",
            "subject": "update email test",
            "body": "update email test",
            "priority": "low"
        }

        # Make a PUT request to update the email
        response = self.client.put(
            f'/emails/detail/{email.pk}/', data=updated_data)

        # Check if the request was successful (HTTP 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the email was updated successfully
        email.refresh_from_db()  # Refresh the email instance from the database
        self.assertEqual(email.subject, updated_data['subject'])

    def test_update_nonexistent_email(self):
        """
        Test that we cannot update a non-existent email
        """

        # Make a PUT request to update a non-existent email
        response = self.client.put('/emails/detail/999/', data={})

        # Check if the request returns a 404 Not Found status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_email(self):
        """
        Test that we can delete an email
        """

        email = Email.objects.create(
            subject='Test Email', sender=self.user, recipient=self.user, status=True)

        # Make a DELETE request to delete the email
        response = self.client.delete(f'/emails/detail/{email.pk}/')

        # Check if the request was successful (HTTP 204)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the email was deleted successfully
        with self.assertRaises(Email.DoesNotExist):
            email.refresh_from_db()

        # Check if the response message is correct
        expected_message = "Email deleted successfully"
        self.assertEqual(response.data['message'], expected_message)

    def test_delete_nonexistent_email(self):
        """
        Test that we cannot delete a non-existent email
        """

        # Make a DELETE request to delete a non-existent email
        response = self.client.delete('/emails/detail/999/')

        # Check if the request returns a 404 Not Found status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check if the response message is correct
        expected_message = "Email does not exist"
        self.assertEqual(response.data['message'], expected_message)

    def test_get_email(self):
        """
        Test that we can retrieve an email
        """

        # Create a test email
        email = Email.objects.create(
            subject='Test Email', sender=self.user, recipient=self.user, status=True)

        # Make a GET request to retrieve the email
        response = self.client.get(f'/emails/detail/{email.pk}/')

        # Check if the request was successful (HTTP 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data matches the expected serialized data
        expected_data = EmailSerializer(email).data
        self.assertEqual(response.data['data'], expected_data)

        # Check if the response message is correct
        expected_message = "Email retrieved successfully"
        self.assertEqual(response.data['message'], expected_message)

    def test_get_nonexistent_email(self):
        """
        Test that we cannot retrieve a non-existent email
        """

        # Make a GET request to retrieve a non-existent email
        response = self.client.get('/emails/detail/999/')

        # Check if the request returns a 404 Not Found status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check if the response message is correct
        expected_message = "Email does not exist"
        self.assertEqual(response.data['message'], expected_message)

    def test_change_email_status(self):
        """
        Test that we can change the status of an email
        """

        # Create a test email
        email = Email.objects.create(
            subject='Test Email', sender=self.user, recipient=self.user, status=False)

        # Make a PUT request to change the email status
        response = self.client.put(f'/emails/status/read/{email.pk}/')

        # Check if the request was successful (HTTP 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the email status was changed successfully
        email.refresh_from_db()  # Refresh the email instance from the database
        self.assertTrue(email.status)

        # Check if the response message is correct
        expected_message = "Email read status changed successfully"
        self.assertEqual(response.data['message'], expected_message)

    def test_change_status_of_nonexistent_email(self):
        """
        Test that we cannot change the status of a non-existent email
        """

        # Make a PUT request to change the status of a non-existent email
        response = self.client.put('/emails/status/read/999/')

        # Check if the request returns a 404 Not Found status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check if the response message is correct
        expected_message = "Email does not exist"
        self.assertEqual(response.data['message'], expected_message)
