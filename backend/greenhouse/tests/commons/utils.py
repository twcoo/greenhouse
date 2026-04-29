import io
import os
import shutil
from urllib.parse import urlparse

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase


class CreateTestImageMixin:
    def create_test_image(
        self,
        name: str = "test",
        extension: str = "png",
        width: int = 800,
        height: int = 600,
        target_mb: float = 2,
    ) -> SimpleUploadedFile:
        ext = extension.lower().replace("jpg", "jpeg")
        filename = f"{name}.{extension}"

        img_byte_arr = io.BytesIO()
        img = Image.new("RGB", (width, height), color="blue")

        img.save(img_byte_arr, format=ext.upper())

        target_bytes = int(target_mb * 1024 * 1024)
        current_size = img_byte_arr.tell()

        if current_size < target_bytes:
            img_byte_arr.write(b"\x00" * (target_bytes - current_size))

        img_byte_arr.seek(0)

        return SimpleUploadedFile(
            name=filename,
            content=img_byte_arr.read(),
            content_type=f"image/{ext}",
        )


class ImageUploadAPITestCase(CreateTestImageMixin, APITestCase):
    upload_to: str

    def setUp(self):
        if not self.upload_to:
            raise ValueError("upload_to must be defined.")

        super().setUp()

    def tearDown(self):
        folder = os.path.join(
            settings.MEDIA_ROOT, getattr(self, "upload_to", "")
        )

        if os.path.isdir(folder):
            shutil.rmtree(folder)

        super().tearDown()

    def upload_image(
        self,
        image_filename: str = "test",
        image_extension: str = "png",
        image_size: float = 2,
    ) -> None:
        image = self.create_test_image(
            name=image_filename, extension=image_extension, target_mb=image_size
        )

        data = {"image": image}

        response = self.client.put(self.url, data, format="multipart")

        response_status, data, message = self.get_response_data(response)

        image = data["image"]

        parsed_image_url_path = urlparse(image).path

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertIsNotNone(image)
        self.assertEqual(
            f"/media/{self.upload_to}/{image_filename}.{image_extension}",
            parsed_image_url_path,
        )
        self.assertIsNone(message)

    def test_upload_png_image_success(self):
        self.authenticate()
        self.upload_image(image_filename="crop_png")

    def test_upload_jpg_image_success(self):
        self.authenticate()
        self.upload_image(image_filename="crop_jpg", image_extension="jpg")
