from .models import TruckDriver
from .models import Company
from django import forms


STATUS_CHOICES = [
    ('','All'),
    ('Waiting', 'Waiting'),
    ('In Progress', 'In Progress'),
    ('Finished', 'Finished'),
]

class TruckDriverForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        label='Company',
        queryset=Company.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        empty_label='Select a company...'
    )
    class Meta:
        model = TruckDriver
        fields = ['name', 'company']
    name = forms.CharField(label='Driver Name', max_length=200,required=True)
    
class MasterReportForm(forms.Form):
    status = forms.ChoiceField(
        label='Status',
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    company = forms.ModelChoiceField(
        label='Company',
        queryset=Company.objects.all().order_by('name'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='All Companies'
    )

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'contact_email', 'total_tests', 'tests_remaining']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email or leave blank'
            }),
            'total_tests': forms.NumberInput(attrs={'class': 'form-control'}),
            'tests_remaining': forms.NumberInput(attrs={'class': 'form-control'}),
        }