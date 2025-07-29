from django.shortcuts import render, redirect, HttpResponse, get_list_or_404, get_object_or_404
from .forms import TruckDriverForm, MasterReportForm, CompanyForm, CompanyEditForm
from .models import TruckDriver
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
import os
from django.utils import timezone
import openpyxl
from openpyxl import Workbook
from django.core.mail import send_mail
from .models import Company
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .email_utils import (
    send_test_started_email,
    send_test_completed_email, 
    send_low_balance_email, 
    send_zero_balance_email, 
    send_welcome_email
)
from datetime import date, timedelta
from django.db.models import Count
from django.db.models import Q

# Create your views here.

# Old email functions removed - now using HTML email system in email_utils.py

def driver_form(request):
    if request.method == 'POST':
        form = TruckDriverForm(request.POST)
        if form.is_valid():
            try:
                driver = form.save(commit=False)
                
                # Get the follow-up value
                is_follow_up = form.cleaned_data.get('is_follow_up', False)
                driver.is_follow_up = is_follow_up
                
                # Handle follow-up logic
                if is_follow_up:
                    # Get or create the FOLLOW-UP company
                    follow_up_company, created = Company.objects.get_or_create(
                        name="FOLLOW-UP",
                        defaults={
                            'contact_email': '',
                            'total_tests': 0,
                            'tests_remaining': 0,
                            'is_active': True
                        }
                    )
                    driver.company = follow_up_company
                else:
                    # Check if selected company has available tests
                    company = form.cleaned_data.get('company')
                    if company and company.tests_remaining <= 0:
                        form.add_error('company', f"Sorry, {company.name} has no tests remaining. Please contact your company administrator.")
                        return render(request, 'driver_form.html', {'form': form})
                
                # Set check-in time and date
                now = timezone.localtime()
                driver.check_in_time = now.time()
                driver.check_in_date = now.date()
                driver.status = 'Waiting'
                
                # Save the driver
                driver.save()
                
                # Send welcome email if company has email
                if driver.company and driver.company.contact_email:
                    try:
                        send_welcome_email(driver.company, driver)
                    except Exception as e:
                        # Log the error but don't fail the form submission
                        print(f"Failed to send welcome email: {e}")
                
                return render(request, 'success.html')
                
            except Exception as e:
                # Handle any unexpected errors
                form.add_error(None, f"An error occurred while processing your submission. Please try again. Error: {str(e)}")
                return render(request, 'driver_form.html', {'form': form})
    else:
        form = TruckDriverForm()

    # Get some context for the template
    context = {
        'form': form,
        'total_drivers_today': TruckDriver.objects.filter(
            check_in_date=timezone.localtime().date()
        ).count(),
        'active_companies': Company.objects.filter(is_active=True).count(),
    }

    return render(request, 'driver_form.html', context)

def success(request):
    return render(request, 'success.html')

def queue_list(request):
    drivers=TruckDriver.objects.exclude(status='Finished')
    return render(request, 'queue_list.html', {'drivers':drivers})


@login_required
def menu(request):
    return render(request, 'menu.html')

@login_required
def manage_queue(request):
    today = timezone.localdate()
    submissions = TruckDriver.objects.exclude(status='Finished').order_by('check_in_date', 'check_in_time')
    
    # Calculate counts for summary cards
    total_in_queue = TruckDriver.objects.exclude(status='Finished').count()
    waiting_count = TruckDriver.objects.filter(status='Waiting').count()
    in_progress_count = TruckDriver.objects.filter(status='In Progress').count()
    finished_today_count = TruckDriver.objects.filter(status='Finished', finished_date=today).count()

    context = {
        'submissions': submissions,
        'total_in_queue': total_in_queue,
        'waiting_count': waiting_count,
        'in_progress_count': in_progress_count,
        'finished_today_count': finished_today_count,
    }

    return render(request, 'manage_queue.html', context)

@require_POST
@login_required 
def update_status(request):
    submission_id = request.POST.get('submission_id')
    new_status = request.POST.get('new_status')

    try:
        submission = get_object_or_404(TruckDriver, id=submission_id)
        original_status = submission.status

        if new_status == 'In Progress' and original_status != 'In Progress':
            submission.status = 'In Progress'
            now = timezone.localtime()
            submission.in_progress_time = now.time()
            submission.in_progress_date = now.date()
            submission.in_progress_employee = request.user.username
            submission.save()
            
            # Send test started notification
            send_test_started_email(submission)

        elif new_status == 'Finished' and original_status != 'Finished':
            submission.status = 'Finished'
            now = timezone.localtime()
            submission.finished_time = now.time()
            submission.finished_date = now.date()
            submission.finished_employee = request.user.username
            submission.save()

            # Send completion notification
            send_test_completed_email(submission)

            # Update test balance and send alerts
            if submission.company and submission.company.tests_remaining > 0:
                submission.company.tests_remaining -= 1
                submission.company.save()

                # Send appropriate balance alerts
                if submission.company.tests_remaining == 0:
                    send_zero_balance_email(submission.company)
                elif submission.company.tests_remaining <= 5:
                    send_low_balance_email(submission.company)

        return JsonResponse({'success': True})

    except TruckDriver.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Submission not found'}, status=404)


@login_required
def check_queue_updates(request):
    """Check for updates in the queue and return the latest update time"""
    from django.utils import timezone
    
    # Get the most recent update time from any driver record
    latest_driver = TruckDriver.objects.order_by('-finished_date', '-finished_time').first()
    
    if latest_driver and latest_driver.finished_date:
        # Use the finished date/time as the last update indicator
        last_update = timezone.make_aware(
            timezone.datetime.combine(latest_driver.finished_date, latest_driver.finished_time or timezone.now().time())
        )
    else:
        # If no finished drivers, use current time
        last_update = timezone.now()
    
    return JsonResponse({
        'last_update': last_update.isoformat(),
        'total_drivers': TruckDriver.objects.count(),
        'waiting_count': TruckDriver.objects.filter(status='Waiting').count(),
        'in_progress_count': TruckDriver.objects.filter(status='In Progress').count(),
        'finished_count': TruckDriver.objects.filter(status='Finished').count(),
    })


@login_required
def report_list(request):
    if request.method == 'POST':
        form=MasterReportForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            drivers = TruckDriver.objects.all()
            if status != '':
                if status == 'Waiting':
                    drivers = drivers.filter(status='Waiting')
                if status == 'In Progress':
                    drivers = drivers.filter(status='In Progress')
                if status == 'Finished':
                    drivers = drivers.filter(status='Finished')
            
        wb = Workbook()
        ws = wb.active
        ws.title = 'Trucker Wait List Report'

        ws.append(['Name', 'Phone Number', 'Company', 'Status', 'Check In Time', 
                    'Check In Date', 'In Progress Time', 'In Progress Date', 'In Progress Employee',
                    'Finished Time', 'Finished Date', 'Finished Employee'])
        for driver in drivers:
            ws.append([driver.name, driver.phone_number or '', driver.company.name if driver.company else '', 
                        driver.status, driver.check_in_time, driver.check_in_date,  
                        driver.in_progress_time, driver.in_progress_date, driver.in_progress_employee,
                        driver.finished_time, driver.finished_date, driver.finished_employee])
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment; filename=TruckerWaitListReport.xlsx" 
            
        wb.save(response)

        return response
    else:
        form = MasterReportForm()
    return render(request, 'report_list.html', {'form': form})

@login_required
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)

            # ✅ Set placeholder email if left blank
            if not company.contact_email:
                company.contact_email = 'placeholder@example.com'

            # Set default value for total_tests (not shown in form)
            company.total_tests = 0

            company.save()
            
            # Send welcome email if company has a real email
            if company.contact_email and company.contact_email.lower() != 'placeholder@example.com':
                send_welcome_email(company)
            
            # Add success message to session
            request.session['success_message'] = f"Company '{company.name}' has been successfully added with {company.tests_remaining} test balance."
            return redirect('menu')
    else:
        form = CompanyForm()

    return render(request, 'add_company.html', {'form': form})

from django.core.paginator import Paginator

@login_required
def modify_companies(request):
    search_query = request.GET.get('q', '')
    companies_list = Company.objects.all().order_by('name')
    if search_query:
        companies_list = companies_list.filter(
            Q(name__icontains=search_query) |
            Q(contact_email__icontains=search_query)
        )
    paginator = Paginator(companies_list, 10)  # Show 10 companies per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate counts for summary cards
    total_companies = Company.objects.count()
    active_companies = Company.objects.filter(is_active=True).count()
    inactive_companies = Company.objects.filter(is_active=False).count()
    low_balance_companies = Company.objects.filter(tests_remaining__lte=5).count()
    
    context = {
        'companies': page_obj,
        'page_obj': page_obj,
        'total_companies': total_companies,
        'active_companies': active_companies,
        'inactive_companies': inactive_companies,
        'low_balance_companies': low_balance_companies,
        'search_query': search_query,
    }
    
    return render(request, 'modify_companies.html', context)

@login_required
def edit_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    
    if request.method == 'POST':
        form = CompanyEditForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            request.session['success_message'] = f"Company '{company.name}' has been successfully updated."
            return redirect('modify_companies')
    else:
        form = CompanyEditForm(instance=company)
    
    return render(request, 'edit_company.html', {
        'form': form,
        'company': company
    })

@login_required
def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    
    if request.method == 'POST':
        company_name = company.name
        company.delete()
        request.session['success_message'] = f"Company '{company_name}' has been successfully deleted."
        return redirect('modify_companies')
    
    return render(request, 'delete_company.html', {
        'company': company
    })

@login_required
def dashboard(request):
    from waitapp.models import TruckDriver, Company
    from django.utils import timezone
    today = timezone.localdate()
    first_of_month = today.replace(day=1)

    # Tests this month
    tests_this_month = TruckDriver.objects.filter(check_in_date__gte=first_of_month).count()

    # Active companies
    active_companies = Company.objects.filter(is_active=True).count()

    # Low balance companies
    low_balance_companies = Company.objects.filter(tests_remaining__lte=5).count()

    # Tests per day (last 14 days)
    tests_per_day_labels = []
    tests_per_day_data = []
    for i in range(13, -1, -1):
        day = today - timedelta(days=i)
        count = TruckDriver.objects.filter(check_in_date=day).count()
        tests_per_day_labels.append(day.strftime('%b %d'))
        tests_per_day_data.append(count)

    # Top 5 companies by test volume (all time)
    top_companies_qs = (TruckDriver.objects
        .values('company__name')
        .annotate(test_count=Count('id'))
        .order_by('-test_count')[:5])
    top_companies_labels = [c['company__name'] or 'No Company' for c in top_companies_qs]
    top_companies_data = [c['test_count'] for c in top_companies_qs]

    # Status breakdown
    status_labels = ['Waiting', 'In Progress', 'Finished']
    status_data = [
        TruckDriver.objects.filter(status='Waiting').count(),
        TruckDriver.objects.filter(status='In Progress').count(),
        TruckDriver.objects.filter(status='Finished').count(),
    ]

    context = {
        'tests_this_month': tests_this_month,
        'active_companies': active_companies,
        'low_balance_companies': low_balance_companies,
        'tests_per_day_labels': tests_per_day_labels,
        'tests_per_day_data': tests_per_day_data,
        'top_companies_labels': top_companies_labels,
        'top_companies_data': top_companies_data,
        'status_labels': status_labels,
        'status_data': status_data,
    }
    # Tests per week (last 8 weeks)
    tests_per_week_labels = []
    tests_per_week_data = []
    for i in range(7, -1, -1):
        week_start = today - timedelta(days=today.weekday() + i * 7)
        week_end = week_start + timedelta(days=6)
        count = TruckDriver.objects.filter(check_in_date__gte=week_start, check_in_date__lte=week_end).count()
        label = week_start.strftime('%b %d')
        tests_per_week_labels.append(label)
        tests_per_week_data.append(count)

    # Tests per month (last 12 months)
    tests_per_month_labels = []
    tests_per_month_data = []
    for i in range(11, -1, -1):
        month = (today.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        next_month = (month + timedelta(days=32)).replace(day=1)
        count = TruckDriver.objects.filter(check_in_date__gte=month, check_in_date__lt=next_month).count()
        label = month.strftime('%b %Y')
        tests_per_month_labels.append(label)
        tests_per_month_data.append(count)

    # Tests by hour of day (0-23)
    tests_by_hour_labels = [f'{h}:00' for h in range(24)]
    tests_by_hour_data = []
    for h in range(24):
        count = TruckDriver.objects.filter(check_in_time__hour=h).count()
        tests_by_hour_data.append(count)

    context.update({
        'tests_per_week_labels': tests_per_week_labels,
        'tests_per_week_data': tests_per_week_data,
        'tests_per_month_labels': tests_per_month_labels,
        'tests_per_month_data': tests_per_month_data,
        'tests_by_hour_labels': tests_by_hour_labels,
        'tests_by_hour_data': tests_by_hour_data,
    })
    return render(request, 'dashboard.html', context)