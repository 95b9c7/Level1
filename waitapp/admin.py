from django.contrib import admin
from .models import TruckDriver, Company

# Register your models here.
@admin.register(TruckDriver)
class TruckDriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'check_in_date', 'check_in_time', 'status', 'in_progress_date', 'in_progress_time', 
                    'in_progress_employee', 'finished_date', 'finished_time', 'finished_employee')
    list_filter = ('in_progress_employee', 'finished_employee', 'company')
    search_fields = ('in_progress_employee', 'finished_employee', 'company')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'total_tests', 'tests_remaining']
