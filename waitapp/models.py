from django.db import models

# Create your models here.
class TruckDriver(models.Model):
    name = models.CharField(max_length=200, default='-')
    #dot_number = models.CharField(max_length=200, default='-')
    company = models.CharField(max_length=200, default='-')
    check_in_date = models.DateField(auto_now_add=True)
    check_in_time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=200, default='Waiting')
    in_progress_date = models.DateField(null=True, blank=True)
    in_progress_time = models.TimeField(null=True, blank=True)
    in_progress_employee = models.CharField(max_length=200, default='-')
    finished_date = models.DateField(null=True, blank=True)
    finished_time = models.TimeField(null=True, blank=True)
    finished_employee = models.CharField(max_length=200, default='-')