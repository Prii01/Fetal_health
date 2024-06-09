from django.contrib import admin
from fetal_health.models import *

class FetalHealthInputAdmin(admin.ModelAdmin):
    list_display = ['user', 'baseline_value', 'fetal_health', 'delivery_type', 'created_at']
    list_filter = ['fetal_health', 'delivery_type']
    search_fields = ['user__username', 'user__email']  # Add fields of the related User model for searching

admin.site.register(FetalHealthInput, FetalHealthInputAdmin)
