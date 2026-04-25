import factory
from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory

from ...models import (Crop, Planting, PlantingLocation,
                       PlantingLocationAssignment, Variety)

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = "shimmer"
    password = "ShimmerDontJump!"
    is_superuser = True
    is_staff = False


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


class PlantingLocationFactory(DjangoModelFactory):
    class Meta:
        model = PlantingLocation

    name = factory.Sequence(lambda n: f"Location {n}")
    location_type = "GROUND"
    width = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )
    length = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )
    height = None


class VarietyFactory(DjangoModelFactory):
    class Meta:
        model = Variety

    name = factory.Sequence(lambda n: f"Variety {n}")
    crop = factory.SubFactory(
        CropFactory,
        user=factory.SubFactory(
            UserFactory,
            username=factory.Sequence(lambda n: f"variety_user_{n}"),
        ),
    )
    growth_habit = ["INDETERMINATE"]


class PlantingFactory(DjangoModelFactory):
    class Meta:
        model = Planting

    user = factory.SubFactory(
        UserFactory,
        username=factory.Sequence(lambda n: f"planting_user_{n}"),
    )
    crop = factory.SubFactory(CropFactory, user=factory.SelfAttribute("..user"))
    variety = factory.SubFactory(
        VarietyFactory, crop=factory.SelfAttribute("..crop")
    )


class PlantingLocationAssignmentFactory(DjangoModelFactory):
    class Meta:
        model = PlantingLocationAssignment

    planting = factory.SubFactory(PlantingFactory)
    planting_location = factory.SubFactory(
        PlantingLocationFactory,
        user=factory.SelfAttribute("..planting.user"),
    )
    start_date = factory.Faker("date_this_decade")
    end_date = None
