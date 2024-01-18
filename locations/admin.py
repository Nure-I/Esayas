from django.contrib import admin
from .models import Location
from django.http import HttpResponse
import csv

class LocationAdmin(admin.ModelAdmin):
    list_display = ("user",'fullName', "name_amharic", 'name_afaan_oromo', 'job_type_amharic','job_type_afaan_oromo','width', 'height', 'square', 'completed')
    search_fields = ('fullName',"name_afaan_oromo","name_amharic", 'job_type_amharic','job_type_afaan_oromo')
    list_filter = ("user",'fullName', 'job_type_amharic')
    actions = ['export_locations']

    def export_locations(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="locations.csv"'

        writer = csv.writer(response)
        # Add all fields dynamically
        field_names = [field.name for field in Location._meta.get_fields()]
        writer.writerow(field_names)

        for location in queryset:
            # Extract values for all fields dynamically
            row = [getattr(location, field) for field in field_names]
            writer.writerow(row)

        return response

    export_locations.short_description = "Export selected locations"

admin.site.register(Location, LocationAdmin)
