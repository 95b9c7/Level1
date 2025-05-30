from waitapp.models import TruckDriver, Company

def run():
    count_linked = 0
    count_created = 0

    for td in TruckDriver.objects.all():
        name = td.company_name.strip()
        if not name:
            continue

        company, created = Company.objects.get_or_create(
            name=name,
            defaults={
                'contact_email': 'placeholder@example.com',
                'total_tests': 0,
                'tests_remaining': 0,
            }
        )

        td.company = company
        td.save()

        count_linked += 1
        if created:
            count_created += 1

    print(f"{count_linked} drivers linked to companies.")
    print(f"{count_created} companies were newly created.")