from django.contrib import admin as admin

from .models import Crop as Crop
from .models import Variety as Variety

admin.site.register(Crop)
admin.site.register(Variety)
