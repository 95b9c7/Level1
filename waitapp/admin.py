from django.contrib import admin
from .models import TruckDriver

# Register your models here.
@admin.register(TruckDriver)
class TruckDriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'dot_number', 'company', 'check_in_date', 'check_in_time', 'status', 'in_progress_date', 'in_progress_time', 
                    'in_progress_employee', 'finished_date', 'finished_time', 'finished_employee')
    list_filter = ('in_progress_employee', 'finished_employee', 'dot_number', 'company')
    search_fields = ('in_progress_employee', 'finished_employee', 'dot_number', 'company')
