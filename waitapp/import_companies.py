from waitapp.models import Company

COMPANY_NAMES = [
    '1 Line', 'AC TRADE', 'AC TRADE MX', 'ANGULO', 'AV TRUCKING', 'AZR EXPRESS',
    'B-MOR', 'BLACK EAGLE', 'BRAVO', 'CANALES CONCRETE', 'CARO-KAR', 'CHAIN SERVICES',
    'CHASE EXPRESS', 'CHIEFY', 'CN EXPRESS', 'CSM LOGISTICS', 'CUCO’S TRUCKING',
    'DANNY’S', 'DCG CARRIERS', 'DEGO TRANSPORT', 'DUBAI / MCSS', 'EC TRANSPORT',
    'EMR', 'EVOLUTION STAR', 'FASTEX LINK LLC', 'FLETES', 'FT LOGISTICS INC', 'FYA',
    'GARWI', 'G&M EMPLOYMENT', 'GLOBAL LINK CARRIERS', 'GOD DID', 'Gonzalez International',
    'HISMAGAN', 'HR VICTORIA', 'JACK GAS + OIL', 'JAIRO OCTAPA', 'JEER', 'JO MA',
    'JOY TRUCKING', 'LAFAYETTE', 'LARA TRANSPORT', 'Luisana Lopez Cano', 'MACIEL',
    'MARVIN', 'MLP XPRESS', 'Mondtur Trucking', 'MVL Transportation', 'NAG GROUP LLC',
    'NATIONAL EXPRESS', 'NAVI FREIGHT', 'NAVI MX', 'PENTAX', 'RAMBRI',
    'Ramirez Truck Lines', 'R2 LOGISTICS', 'RF CARRIERS', 'RGF Cargo', 'ROAD DLC',
    'ROBMAR', 'RM PERSONNEL', 'SIMA', 'SDL CARRIERS', 'Servicio De Transfer', 'STX BORDER',
    'TEAM MARTINEZ', 'TRANSPORTES CAAM', 'VESTA', 'VILLAREAL TOWING', 'WARRIORS',
    'WOOD PALLETE', 'XLR8 Logistics LLC', 'ZACO'
]

def run():
    created_count = 0

    for name in COMPANY_NAMES:
        obj, created = Company.objects.get_or_create(
            name=name,
            defaults={
                'contact_email': 'placeholder@example.com',
                'total_tests': 0,
                'tests_remaining': 0
            }
        )
        if created:
            created_count += 1

    print(f"{created_count} new companies were created.")