from django.contrib import admin as admin

from .models import (Crop, Planting, PlantingDailyObservation,
                     PlantingGrowthStage, PlantingLocation,
                     PlantingLocationAssignment, PlantingLocationStatus,
                     Variety)

admin.site.register(Crop)
admin.site.register(Variety)
admin.site.register(Planting)
admin.site.register(PlantingDailyObservation)
admin.site.register(PlantingGrowthStage)
admin.site.register(PlantingLocation)
admin.site.register(PlantingLocationAssignment)
admin.site.register(PlantingLocationStatus)
