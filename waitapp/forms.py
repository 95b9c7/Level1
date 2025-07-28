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
    class Meta:
        model = TruckDriver
        fields = ['name', 'company', 'phone_number', 'is_follow_up']
    name = forms.CharField(
        label='Driver Name', 
        max_length=200,
        required=True
    )
    company = forms.ModelChoiceField(
        label='Company',
        queryset=Company.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label='Select a company...'
    )
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )

    is_follow_up = forms.BooleanField(
        label='Follow-up?',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


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
        fields = ['name', 'contact_email', 'tests_remaining']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email or leave blank'
            }),
            'tests_remaining': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tests_remaining'].label = 'Test Balance'