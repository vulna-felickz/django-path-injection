from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from pathlib import Path

class FileManagerDownloadViewTests(TestCase):
    def setUp(self):
        self.local_volume_path = Path("/root/my_django_project/files")
        self.valid_subdir = "test_subdir"
        self.valid_filename = "test_file.txt"
        self.invalid_subdir = "invalid_subdir"
        self.invalid_filename = "invalid_file.txt"

        # Create a test directory and file
        os.makedirs(self.local_volume_path / self.valid_subdir, exist_ok=True)
        with open(self.local_volume_path / self.valid_subdir / self.valid_filename, 'w') as f:
            f.write("This is a test file.")

    def tearDown(self):
        # Clean up the test directory and file
        try:
            os.remove(self.local_volume_path / self.valid_subdir / self.valid_filename)
            os.rmdir(self.local_volume_path / self.valid_subdir)
        except Exception:
            pass

    def test_download_valid_file(self):
        response = self.client.post(reverse('file_download'), {'subdir': self.valid_subdir, 'filename': self.valid_filename})
        self.assertEqual(response.status_code, 200)

    def test_download_invalid_file(self):
        response = self.client.post(reverse('file_download'), {'subdir': self.valid_subdir, 'filename': self.invalid_filename})
        self.assertEqual(response.status_code, 404)

    def test_download_invalid_subdir(self):
        response = self.client.post(reverse('file_download'), {'subdir': self.invalid_subdir, 'filename': self.valid_filename})
        self.assertEqual(response.status_code, 404)

    def test_missing_filename(self):
        response = self.client.post(reverse('file_download'), {'subdir': self.valid_subdir})
        self.assertEqual(response.status_code, 400)

    def test_missing_subdir(self):
        response = self.client.post(reverse('file_download'), {'filename': self.valid_filename})
        self.assertEqual(response.status_code, 400)