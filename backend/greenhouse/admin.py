from django.contrib import admin as admin

from .models import (Crop, Fertilizer, FertilizerLog, Planting,
                     PlantingDailyObservation, PlantingGrowthStage,
                     PlantingLocation, PlantingLocationAssignment,
                     PlantingLocationStatus, Variety)

admin.site.register(Crop)
admin.site.register(Fertilizer)
admin.site.register(FertilizerLog)
admin.site.register(Variety)
admin.site.register(Planting)
admin.site.register(PlantingDailyObservation)
admin.site.register(PlantingGrowthStage)
admin.site.register(PlantingLocation)
admin.site.register(PlantingLocationAssignment)
admin.site.register(PlantingLocationStatus)
