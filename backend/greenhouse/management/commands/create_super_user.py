from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from loguru import logger


class Command(BaseCommand):
    help = "Create a superuser if one does not exist"

    def handle(self, *args, **kwargs) -> None:
        User = get_user_model()

        email = config("SUPERUSER_EMAIL")
        username = config("SUPERUSER_USERNAME")
        password = config("SUPERUSER_PASSWORD")

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email, username=username, password=password
            )
            logger.info(f'Superuser "{email}" created.')
        else:
            logger.info(f'Superuser "{email}" already exists.')
