from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help: str = "Runs initial setup"

    def handle(self, *args, **kwargs) -> None:
        call_command("makemigrations", "--noinput")
        call_command("migrate")
