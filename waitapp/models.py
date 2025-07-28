from django.db import models

# Create your models here.
class TruckDriver(models.Model):
    name = models.CharField(max_length=200, default='-')
    #dot_number = models.CharField(max_length=200, default='-')
    #company_name = models.CharField(max_length=200, default='-')
    company = models.ForeignKey('Company', null=True, blank=True, on_delete=models.SET_NULL)
    check_in_date = models.DateField(null=True, blank=True)
    check_in_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=200, default='Waiting')
    in_progress_date = models.DateField(null=True, blank=True)
    in_progress_time = models.TimeField(null=True, blank=True)
    in_progress_employee = models.CharField(max_length=200, default='-')
    finished_date = models.DateField(null=True, blank=True)
    finished_time = models.TimeField(null=True, blank=True)
    finished_employee = models.CharField(max_length=200, default='-')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_follow_up = models.BooleanField(default=False)
    
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_email = models.EmailField(blank=True, null=True)  # ✅ allow blank
    total_tests = models.IntegerField(default=0)
    tests_remaining = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
