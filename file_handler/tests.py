import os
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, mock_open


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('file_handler.views.upload')
    def test_upload_files(self, mock_upload):
        mock_upload.return_value = "test_file.txt"
        url = reverse('upload_files')
        file = SimpleUploadedFile("test_file.txt", "file_content".encode('utf-8'))

        response = self.client.post(url, {'file': file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'uploaded')
        mock_upload.assert_called_once()

    @patch('file_handler.views.is_file_exist')
    @patch('file_handler.views.get_file_content')
    def test_random_line(self, mock_get_content, mock_file_exist):
        mock_file_exist.return_value = True
        mock_get_content.return_value = ["line1\n", "line2\n", "line3\n"]

        url = reverse('random_line', args=['test_file.txt'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('line_number', response.data)
        self.assertIn('file_name', response.data)
        self.assertIn('random_line', response.data)
        self.assertIn('most_frequent_char', response.data)
        self.assertIn(response.data['random_line'], ["line1", "line2", "line3"])

    @patch('file_handler.views.is_file_exist')
    @patch('file_handler.views.get_file_content')
    def test_random_line_backwards(self, mock_get_content, mock_file_exist):
        mock_file_exist.return_value = True
        mock_get_content.return_value = ["line1\n", "line2\n", "line3\n"]

        url = reverse('random_line_backwards', args=['test_file.txt'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('line_number', response.data)
        self.assertIn('file_name', response.data)
        self.assertIn('random_line', response.data)
        self.assertIn('most_frequent_char', response.data)
        self.assertIn(response.data['random_line'], ["1enil", "2enil", "3enil"])

    @patch('os.listdir')
    @patch('file_handler.views.get_file_content')
    def test_longest_100_lines(self, mock_get_file_content, mock_listdir):
        mock_listdir.side_effect = ['file1.txt', 'file2.txt']
        mock_get_file_content.side_effect = [
            ["short\n", "long line\n", "longest line ever\n"],
            ["another\n", "really long line\n", "short\n"]
        ]

        url = reverse('longest_100_lines')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertLessEqual(len(response.data), 100)
        self.assertEqual(response.data[0], "longest line ever\n")

    @patch('file_handler.views.is_file_exist')
    @patch('file_handler.views.get_file_content')
    def test_longest_20_lines(self, mock_get_content, mock_file_exist):
        mock_file_exist.return_value = True
        mock_get_content.return_value = ["short\n", "long line\n", "longest line ever\n", "another line\n"]

        url = reverse('longest_20_lines', args=['test_file.txt'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertLessEqual(len(response.data), 20)
        self.assertEqual(response.data[0], "longest line ever\n")

    @patch('file_handler.views.is_file_exist')
    def test_file_not_found(self, mock_file_exist):
        mock_file_exist.return_value = False
        url = reverse('random_line', args=['nonexistent_file.txt'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('file_handler.views.is_file_exist')
    @patch('file_handler.views.get_file_content')
    def test_empty_file(self, mock_get_content, mock_file_exist):
        mock_file_exist.return_value = True
        mock_get_content.return_value = []

        url = reverse('random_line', args=['empty_file.txt'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('file_handler.views.is_file_exist')
    @patch('file_handler.views.get_file_content')
    def test_plain_text_response(self, mock_get_content, mock_file_exist):
        mock_file_exist.return_value = True
        mock_get_content.return_value = ["line1\n", "line2\n", "line3\n"]

        url = reverse('random_line', args=['test_file.txt'])
        response = self.client.get(url, HTTP_ACCEPT='text/plain')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.content, bytes)
        self.assertIn(response.content.decode(), ["line1", "line2", "line3"])