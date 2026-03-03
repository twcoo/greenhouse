import io

from django.core.files.uploadedfile import SimpleUploadedFile
from knox.models import AuthToken
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from .factories import UserFactory


class RequiredAuthTestsMixin:
    url: str
    http_method: str = "GET"

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.token_instance, self.token = AuthToken.objects.create(self.user)

    def _request(self):
        return self.client.generic(method=self.http_method, path=self.url)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_required_auth_header(self):
        response = self._request()

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response_json["data"])
        self.assertEqual(
            response_json["message"],
            "Authentication credentials were not provided.",
        )

    def test_required_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token Invalid Token")

        response = self._request()

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response_json["data"])
        self.assertEqual(response_json["message"], "Invalid token.")


class ResponseUtilsMixin:
    def validate_no_cross_user_data_leakage(self, user_data, another_user_data):
        returned_ids = {row["id"] for row in user_data}
        another_user_ids = {row.id for row in another_user_data}
        self.assertTrue(returned_ids.isdisjoint(another_user_ids))

    def get_response_data_many(self, response):
        response_json = response.json()

        return (
            response_json["status"],
            response_json["data"],
            response_json["data"]["results"],
            response_json["message"],
        )

    def get_response_data(self, response):
        response_json = response.json()

        return (
            response_json["status"],
            response_json["data"],
            response_json["message"],
        )


class ImageUploadTestMixin:
    def setUp(self):
        super().setUp()

        if not self.upload_to:
            raise ValueError("upload_to must be defined.")

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

    def upload_image(
        self, image_filename="test", image_extension="png", image_size=2
    ):
        image = self.create_test_image(
            name=image_filename, extension=image_extension, target_mb=image_size
        )

        data = {"image": image}

        response = self.client.put(self.url, data, format="multipart")

        response_status, data, message = self.get_response_data(response)

        image = data["image"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_status, "success")
        self.assertIsNotNone(image)
        self.assertEqual(
            f"http://testserver/media/{self.upload_to}/{image_filename}.{image_extension}",
            image,
        )
        self.assertIsNone(message)

    def test_upload_png_image_success(self):
        self.authenticate()
        self.upload_image(image_filename="crop_png")

    def test_upload_jpg_image_success(self):
        self.authenticate()
        self.upload_image(image_filename="crop_jpg", image_extension="jpg")
