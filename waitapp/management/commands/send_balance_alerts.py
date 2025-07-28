from django.core.management.base import BaseCommand
from waitapp.models import Company
from waitapp.email_utils import send_low_balance_email, send_zero_balance_email


class Command(BaseCommand):
    help = 'Send balance alerts to companies with low or zero test balances'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending emails',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Get companies with zero balance
        zero_balance_companies = Company.objects.filter(
            tests_remaining=0,
            is_active=True
        ).exclude(contact_email='placeholder@example.com')
        
        # Get companies with low balance (1-5 tests)
        low_balance_companies = Company.objects.filter(
            tests_remaining__gte=1,
            tests_remaining__lte=5,
            is_active=True
        ).exclude(contact_email='placeholder@example.com')
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would send {zero_balance_companies.count()} zero balance alerts'
                )
            )
            for company in zero_balance_companies:
                self.stdout.write(f'  - {company.name} (0 tests)')
            
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would send {low_balance_companies.count()} low balance alerts'
                )
            )
            for company in low_balance_companies:
                self.stdout.write(f'  - {company.name} ({company.tests_remaining} tests)')
        else:
            # Send zero balance alerts
            zero_count = 0
            for company in zero_balance_companies:
                try:
                    send_zero_balance_email(company)
                    zero_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Sent zero balance alert to {company.name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to send zero balance alert to {company.name}: {e}')
                    )
            
            # Send low balance alerts
            low_count = 0
            for company in low_balance_companies:
                try:
                    send_low_balance_email(company)
                    low_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Sent low balance alert to {company.name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to send low balance alert to {company.name}: {e}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Balance alerts sent: {zero_count} zero balance, {low_count} low balance'
                )
            ) 