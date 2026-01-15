from django.contrib import admin
from baby_tracker_app.models import Baby, Growth, Sleep, Feeding

admin.site.register(Baby)
admin.site.register(Growth)
admin.site.register(Sleep)
admin.site.register(Feeding)
