"""
Email utilities for sending HTML emails
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_html_email(subject, template_name, context, to_email, from_email=None):
    """
    Send an HTML email using Django templates
    
    Args:
        subject (str): Email subject
        template_name (str): Template name (e.g., 'emails/test_completed.html')
        context (dict): Template context variables
        to_email (str): Recipient email address
        from_email (str): Sender email address (optional)
    """
    if from_email is None:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'service@level1da.com')
    
    # Add subject to context for template
    context['subject'] = subject
    
    # Render HTML content
    html_content = render_to_string(template_name, context)
    
    # Create plain text version by stripping HTML tags
    text_content = strip_tags(html_content)
    
    # Create email message
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[to_email]
    )
    
    # Attach HTML version
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    email.send(fail_silently=True)
    
    return email


def send_test_started_email(driver):
    """Send HTML test started email"""
    if not (driver.company and driver.company.contact_email and 
            driver.company.contact_email.lower() != 'placeholder@example.com'):
        return
    
    context = {
        'company_name': driver.company.name,
        'driver_name': driver.name,
        'test_date': driver.in_progress_date,
        'test_time': driver.in_progress_time,
        'admin_employee': driver.in_progress_employee,
        'tests_remaining': driver.company.tests_remaining,
    }
    
    subject = f"Drug Test Started: {driver.name}"
    send_html_email(subject, 'emails/test_started.html', context, driver.company.contact_email)


def send_test_completed_email(driver):
    """Send HTML test completion email"""
    if not (driver.company and driver.company.contact_email and 
            driver.company.contact_email.lower() != 'placeholder@example.com'):
        return
    
    context = {
        'company_name': driver.company.name,
        'driver_name': driver.name,
        'test_date': driver.finished_date,
        'test_time': driver.finished_time,
        'admin_employee': driver.finished_employee,
        'tests_remaining': driver.company.tests_remaining,
    }
    
    subject = f"Drug Test Completed: {driver.name}"
    send_html_email(subject, 'emails/test_completed.html', context, driver.company.contact_email)


def send_low_balance_email(company):
    """Send HTML low balance alert email"""
    if not (company.contact_email and company.contact_email.lower() != 'placeholder@example.com'):
        return
    
    context = {
        'company_name': company.name,
        'tests_remaining': company.tests_remaining,
        'contact_email': company.contact_email,
    }
    
    subject = f"Low Test Balance Alert: {company.name}"
    send_html_email(subject, 'emails/low_balance_alert.html', context, company.contact_email)


def send_zero_balance_email(company):
    """Send HTML zero balance alert email"""
    if not (company.contact_email and company.contact_email.lower() != 'placeholder@example.com'):
        return
    
    context = {
        'company_name': company.name,
        'tests_remaining': company.tests_remaining,
        'contact_email': company.contact_email,
    }
    
    subject = f"URGENT: No Tests Remaining - {company.name}"
    send_html_email(subject, 'emails/zero_balance_alert.html', context, company.contact_email)


def send_welcome_email(company):
    """Send HTML welcome email to new company"""
    if not (company.contact_email and company.contact_email.lower() != 'placeholder@example.com'):
        return
    
    context = {
        'company_name': company.name,
        'tests_remaining': company.tests_remaining,
        'contact_email': company.contact_email,
    }
    
    subject = f"Welcome to Level 1 D&A - {company.name}"
    send_html_email(subject, 'emails/welcome_company.html', context, company.contact_email) 