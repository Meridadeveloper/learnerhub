from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import *

class YourAppTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_user_registration_view(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'nickname': 'TestNickname',
            'title': 'TestTitle',
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'country': 'TestCountry',
            'city': 'TestCity',
            'university': 'TestUniversity',
        }
        response = self.client.post(reverse('user-registration'), data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 201)

        # Add more assertions based on your expected behavior

    def test_user_verification_view(self):
        temp_user = TempUser.objects.create(username='testuser', email='test@example.com', password='testpassword')
        temp_user.otp = '123456'
        temp_user.save()

        data = {
            'username': 'testuser',
            'otp': '123456',
        }
        response = self.client.post(reverse('user-registration'), data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, 200)

    #     # Add more assertions based on your expected behavior

    # def test_login_view(self):
    #     data = {
    #         'username': 'testuser',
    #         'password': 'testpassword',
    #     }
    #     response = self.client.post(reverse('login'), data, format='json')
    #     self.assertEqual(response.status_code, 200)

    #     # Add more assertions based on your expected behavior

    # def test_logout_view(self):
    #     response = self.client.post(reverse('logout'))
    #     self.assertEqual(response.status_code, 200)

    #     # Add more assertions based on your expected behavior

    # def test_studies_view(self):
    #     data = {
    #         'degree': 'TestDegree',
    #         'program': 'TestProgram',
    #         'year': 'TestYear',
    #     }
    #     response = self.client.post(reverse('studies', args=['testuser']), data, format='json')
    #     self.assertEqual(response.status_code, 200)

    #     # Add more assertions based on your expected behavior

    # def test_document_upload_view(self):
    #     file_path = 'path/to/your/test/pdf/file.pdf'
    #     with open(file_path, 'rb') as pdf_file:
    #         data = {
    #             'file': pdf_file,
    #             'title': 'TestDocumentTitle',
    #         }
    #         response = self.client.post(reverse('document-upload', args=['testuser']), data, format='multipart')
    #         self.assertEqual(response.status_code, 200)

    #     # Add more assertions based on your expected behavior

    # def test_document_display_view(self):
    #     response = self.client.get(reverse('document-display', args=['testuser']))
    #     self.assertEqual(response.status_code, 200)

    #     # Add more assertions based on your expected behavior

    # def test_generate_content_view(self):
    #     data = {
    #         'question': 'TestQuestion',
    #     }
    #     response = self.client.post(reverse('generate-content'), data, format='json')
    #     self.assertEqual(response.status_code, 200)

    #     # Add more assertions based on your expected behavior

    # def test_translate_pdf_view(self):
    #     file_path = 'path/to/your/test/pdf/file.pdf'
    #     with open(file_path, 'rb') as pdf_file:
    #         data = {
    #             'file': pdf_file,
    #             'language': 'fr',  # Change to the language code you want to test
    #         }
    #         response = self.client.get(reverse('translate-pdf', args=['testuser', 1]), data, format='multipart')
    #         self.assertEqual(response.status_code, 200)

    #     # Add more assertions based on your expected behavior

    # def test_universities_view(self):
    #     response = self.client.get(reverse('universities'))
    #     self.assertEqual(response.status_code, 200)

    #     # Add more assertions based on your expected behavior

    # def test_courses_view(self):
    #     response = self.client.get(reverse('courses', args=['TestUniversity']))
    #     self.assertEqual(response.status_code, 200)

    #     # Add more assertions based on your expected behavior
