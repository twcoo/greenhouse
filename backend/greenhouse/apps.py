from django.apps import AppConfig


class GreenhouseConfig(AppConfig):
    name = "greenhouse"

    def ready(self) -> None:
        import greenhouse.signals  # noqa: F401
