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
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'autocomplete': 'name',
            'autofocus': True
        })
    )
    
    company = forms.ModelChoiceField(
        label='Company',
        queryset=Company.objects.filter(is_active=True).order_by('name'),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select your company'
        }),
        required=False,
        empty_label='Select a company...'
    )
    
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(555) 123-4567',
            'autocomplete': 'tel',
            'pattern': '[0-9]{3}-[0-9]{3}-[0-9]{4}'
        })
    )

    is_follow_up = forms.BooleanField(
        label='Follow-up?',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'follow-up-checkbox'
        })
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Remove extra whitespace
            name = ' '.join(name.split())
            # Check if name is too short
            if len(name) < 2:
                raise forms.ValidationError("Name must be at least 2 characters long.")
            # Check if name contains only letters, spaces, and common punctuation
            if not all(c.isalpha() or c.isspace() or c in ".-'" for c in name):
                raise forms.ValidationError("Name can only contain letters, spaces, and common punctuation.")
        return name

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove all non-digit characters
            digits = ''.join(filter(str.isdigit, phone))
            # Check if we have exactly 10 digits
            if len(digits) != 10:
                raise forms.ValidationError("Phone number must be exactly 10 digits.")
            # Format the phone number
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        return phone

    def clean(self):
        cleaned_data = super().clean()
        is_follow_up = cleaned_data.get('is_follow_up')
        company = cleaned_data.get('company')
        
        # If it's a follow-up, company is not required
        if not is_follow_up and not company:
            raise forms.ValidationError("Please select a company or check the follow-up option.")
        
        return cleaned_data


class MasterReportForm(forms.Form):
    status = forms.ChoiceField(
        label='Status',
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    company = forms.ModelChoiceField(
        label='Company',
        queryset=Company.objects.filter(is_active=True).order_by('name'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='All Companies'
    )

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'contact_email', 'tests_remaining']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email or leave blank'
            }),
            'tests_remaining': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tests_remaining'].label = 'Test Balance'
        self.fields['name'].label = 'Company Name'
        self.fields['contact_email'].label = 'Contact Email'
        
        # Make name required and add validation
        self.fields['name'].required = True
        self.fields['tests_remaining'].required = True
        self.fields['contact_email'].required = False
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Check if company with this name already exists
            if Company.objects.filter(name__iexact=name).exists():
                raise forms.ValidationError("A company with this name already exists.")
        return name
    
    def clean_tests_remaining(self):
        tests = self.cleaned_data.get('tests_remaining')
        if tests is not None and tests < 0:
            raise forms.ValidationError("Test balance cannot be negative.")
        return tests

class CompanyEditForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'contact_email', 'tests_remaining', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email or leave blank'
            }),
            'tests_remaining': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter test balance',
                'min': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tests_remaining'].label = 'Test Balance'
        self.fields['name'].label = 'Company Name'
        self.fields['contact_email'].label = 'Contact Email'
        self.fields['is_active'].label = 'Active Company'
        
        # Make name required and add validation
        self.fields['name'].required = True
        self.fields['tests_remaining'].required = True
        self.fields['contact_email'].required = False
        self.fields['is_active'].required = False
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Check if company with this name already exists (excluding current instance)
            existing_companies = Company.objects.filter(name__iexact=name)
            if self.instance.pk:
                existing_companies = existing_companies.exclude(pk=self.instance.pk)
            
            if existing_companies.exists():
                raise forms.ValidationError("A company with this name already exists.")
        return name
    
    def clean_tests_remaining(self):
        tests = self.cleaned_data.get('tests_remaining')
        if tests is not None and tests < 0:
            raise forms.ValidationError("Test balance cannot be negative.")
        return tests