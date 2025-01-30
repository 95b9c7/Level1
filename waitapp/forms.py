from .models import TruckDriver
from django import forms


STATUS_CHOICES = [
    ('Waiting', 'Waiting'),
    ('In Progress', 'In Progress'),
    ('Finished', 'Finished'),
    ('','-')
]

class TruckDriverForm(forms.ModelForm):
    class Meta:
        model = TruckDriver
        fields = ['name', 'dot_number', 'company']
    name = forms.CharField(label='Driver Name', max_length=200,required=True)
    dot_number = forms.CharField(label='DOT Number', max_length=200,required=True)
    company = forms.CharField(label='Company', max_length=200,required=True)
    
class MasterReportForm(forms.Form):
    status = forms.CharField(label='Status', required=False, max_length=200)
