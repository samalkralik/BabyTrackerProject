from django.contrib import admin
from baby_tracker_app.models import Baby, GrowthMilestones, Sleep, Feeding

admin.site.register(Baby)
admin.site.register(GrowthMilestones)
admin.site.register(Sleep)
admin.site.register(Feeding)
