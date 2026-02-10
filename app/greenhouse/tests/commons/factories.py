import factory
from factory import Faker
from factory.django import DjangoModelFactory

from ...models import Crop


class CropFactory(DjangoModelFactory):
    class Meta:
        model = Crop

    name = factory.Sequence(lambda n: f"Crop {n}")
    scientific_name = factory.Sequence(lambda n: f"Crop scientificus {n}")
    category = factory.Iterator([choice[0] for choice in Crop.CATEGORY_CHOICES])
    sunlight_requirement = factory.Iterator(
        [choice[0] for choice in Crop.SUNLIGHT_REQUIREMENT_CHOICES]
    )
    min_days_to_harvest = Faker("random_int", min=20, max=60)
    max_days_to_harvest = factory.LazyAttribute(
        lambda obj: obj.min_days_to_harvest + 40
    )
