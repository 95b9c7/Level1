"""
Email configuration for Level 1 D&A Trucker Wait List System
"""

# Email Settings
DEFAULT_FROM_EMAIL = 'zrincon@level1da.com'
SUPPORT_EMAIL = 'service@level1da.com'
SUPPORT_PHONE = '(956) 237-7155'  # Replace with actual phone number

# Email Templates
EMAIL_TEMPLATES = {
    'welcome': {
        'subject': 'Welcome to Level 1 D&A - {company_name}',
        'template': 'welcome_email.html'
    },
    'test_started': {
        'subject': 'Drug Test Started: {driver_name}',
        'template': 'test_started_email.html'
    },
    'test_completed': {
        'subject': 'Drug Test Completed: {driver_name}',
        'template': 'test_completed_email.html'
    },
    'low_balance': {
        'subject': 'Low Test Balance Alert: {company_name}',
        'template': 'low_balance_email.html'
    },
    'zero_balance': {
        'subject': 'URGENT: No Tests Remaining - {company_name}',
        'template': 'zero_balance_email.html'
    }
}

# Balance Alert Thresholds
LOW_BALANCE_THRESHOLD = 5  # Send alert when ≤5 tests remaining
ZERO_BALANCE_THRESHOLD = 0  # Send urgent alert when 0 tests remaining

# Email Frequency Settings
DAILY_BALANCE_ALERTS = True  # Send daily balance alerts to companies with low balance
WEEKLY_SUMMARY = True  # Send weekly summary emails to companies 