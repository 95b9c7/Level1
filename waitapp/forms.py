from .models import TruckDriver
from .models import Company
from django import forms


STATUS_CHOICES = [
    ('','All'),
    ('Waiting', 'Waiting'),
    ('In Progress', 'In Progress'),
    ('Finished', 'Finished'),
]

COMPANY_CHOICES = [
    ('', 'Select a company...'),
    ('1 Line', '1 Line'),
    ('AC TRADE', 'AC TRADE'),
    ('AC TRADE MX', 'AC TRADE MX'),
    ('ANGULO', 'ANGULO'),
    ('AV TRUCKING', 'AV TRUCKING'),
    ('AZR EXPRESS', 'AZR EXPRESS'),
    ('B-MOR', 'B-MOR'),
    ('BLACK EAGLE', 'BLACK EAGLE'),
    ('BRAVO', 'BRAVO'),
    ('CANALES CONCRETE', 'CANALES CONCRETE'),
    ('CARO-KAR', 'CARO-KAR'),
    ('CHAIN SERVICES', 'CHAIN SERVICES'),
    ('CHASE EXPRESS', 'CHASE EXPRESS'),
    ('CHIEFY', 'CHIEFY'),
    ('CN EXPRESS', 'CN EXPRESS'),
    ('CSM LOGISTICS', 'CSM LOGISTICS'),
    ('CUCO’S TRUCKING', 'CUCO’S TRUCKING'),
    ('DANNY’S', 'DANNY’S'),
    ('DCG CARRIERS', 'DCG CARRIERS'),
    ('DEGO TRANSPORT', 'DEGO TRANSPORT'),
    ('DUBAI / MCSS', 'DUBAI / MCSS'),
    ('EC TRANSPORT', 'EC TRANSPORT'),
    ('EMR', 'EMR'),
    ('EVOLUTION STAR', 'EVOLUTION STAR'),
    ('FASTEX LINK LLC', 'FASTEX LINK LLC'),
    ('FLETES', 'FLETES'),
    ('FT LOGISTICS INC', 'FT LOGISTICS INC'),
    ('FYA', 'FYA'),
    ('GARWI', 'GARWI'),
    ('G&M EMPLOYMENT', 'G&M EMPLOYMENT'),
    ('GLOBAL LINK CARRIERS', 'GLOBAL LINK CARRIERS'),
    ('GOD DID', 'GOD DID'),
    ('Gonzalez International', 'Gonzalez International'),
    ('HISMAGAN', 'HISMAGAN'),
    ('HR VICTORIA', 'HR VICTORIA'),
    ('JACK GAS + OIL', 'JACK GAS + OIL'),
    ('JAIRO OCTAPA', 'JAIRO OCTAPA'),
    ('JEER', 'JEER'),
    ('JO MA', 'JO MA'),
    ('JOY TRUCKING', 'JOY TRUCKING'),
    ('LAFAYETTE', 'LAFAYETTE'),
    ('LARA TRANSPORT', 'LARA TRANSPORT'),
    ('Luisana Lopez Cano', 'Luisana Lopez Cano'),
    ('MACIEL', 'MACIEL'),
    ('MARVIN', 'MARVIN'),
    ('MLP XPRESS', 'MLP XPRESS'),
    ('Mondtur Trucking', 'Mondtur Trucking'),
    ('MVL Transportation', 'MVL Transportation'),
    ('NAG GROUP LLC', 'NAG GROUP LLC'),
    ('NATIONAL EXPRESS', 'NATIONAL EXPRESS'),
    ('NAVI FREIGHT', 'NAVI FREIGHT'),
    ('NAVI MX', 'NAVI MX'),
    ('PENTAX', 'PENTAX'),
    ('RAMBRI', 'RAMBRI'),
    ('Ramirez Truck Lines', 'Ramirez Truck Lines'),
    ('R2 LOGISTICS', 'R2 LOGISTICS'),
    ('RF CARRIERS', 'RF CARRIERS'),
    ('RGF Cargo', 'RGF Cargo'),
    ('ROAD DLC', 'ROAD DLC'),
    ('ROBMAR', 'ROBMAR'),
    ('RM PERSONNEL', 'RM PERSONNEL'),
    ('SIMA', 'SIMA'),
    ('SDL CARRIERS', 'SDL CARRIERS'),
    ('Servicio De Transfer', 'Servicio De Transfer'),
    ('STX BORDER', 'STX BORDER'),
    ('TEAM MARTINEZ', 'TEAM MARTINEZ'),
    ('TRANSPORTES CAAM', 'TRANSPORTES CAAM'),
    ('VESTA', 'VESTA'),
    ('VILLAREAL TOWING', 'VILLAREAL TOWING'),
    ('WARRIORS', 'WARRIORS'),
    ('WOOD PALLETE', 'WOOD PALLETE'),
    ('XLR8 Logistics LLC', 'XLR8 Logistics LLC'),
    ('ZACO', 'ZACO'),
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