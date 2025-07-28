from django.shortcuts import render, redirect, HttpResponse, get_list_or_404, get_object_or_404
from .forms import TruckDriverForm, MasterReportForm, CompanyForm
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

# Create your views here.

def notify_company(driver):
    if (
        driver.company 
        and driver.company.contact_email
        and driver.company.contact_email.lower() != "placeholder@example.com"
        ):
        subject = f"Drug Test Completed: {driver.name}"
        message = (
            f"Hello {driver.company.name},\n\n"
            f"{driver.name} has completed a drug test on {driver.finished_date} at {driver.finished_time}.\n\n"
            f"Thank you,\nTrucker Wait List System"
        )

        send_mail(
            subject,
            message,
            'zrincon@level1da.com',  # You can customize this
            [driver.company.contact_email],
            fail_silently=True,
        )

def driver_form(request):
    if request.method == 'POST':
        form = TruckDriverForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            
            # Handle follow-up logic
            if driver.is_follow_up:
                # Get or create the FOLLOW-UP company
                follow_up_company, created = Company.objects.get_or_create(
                    name="FOLLOW-UP",
                    defaults={
                        'contact_email': '',
                        'total_tests': 0,
                        'tests_remaining': 0
                    }
                )
                driver.company = follow_up_company
            
            now = timezone.localtime()
            driver.check_in_time = now.time()
            driver.check_in_date = now.date()
            driver.save()
            return render(request, 'success.html')
    else:
        form = TruckDriverForm()

    return render(request, 'driver_form.html', {'form': form})

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
    submissions = TruckDriver.objects.exclude(status='Finished').order_by('check_in_date', 'check_in_time')

    return render(request, 'manage_queue.html', {'submissions': submissions})

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

        elif new_status == 'Finished' and original_status != 'Finished':
            submission.status = 'Finished'
            now = timezone.localtime()
            submission.finished_time = now.time()
            submission.finished_date = now.date()
            submission.finished_employee = request.user.username
            submission.save()

            notify_company(submission)  # your custom notification logic

            if submission.company and submission.company.tests_remaining > 0:
                submission.company.tests_remaining -= 1
                submission.company.save()

                if submission.company.tests_remaining <= 5:
                    send_mail(
                        subject=f"Low Test Balance Alert for {submission.company.name}",
                        message=(
                            f"Hello {submission.company.name},\n\n"
                            f"You have {submission.company.tests_remaining} drug tests remaining.\n"
                            f"Please consider purchasing more tests to avoid interruptions.\n\n"
                            f"— Trucker Wait List System"
                        ),
                        from_email='zrincon@level1da.com',
                        recipient_list=[submission.company.contact_email],
                        fail_silently=True,
                    )

        return JsonResponse({'success': True})

    except TruckDriver.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Submission not found'}, status=404)


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

        ws.append(['Name', 'Company', 'Status', 'Check In Time', 
                    'Check In Date', 'In Progress Time', 'In Progress Date', 'In Progress Employee',
                    'Finished Time', 'Finished Date', 'Finished Employee'])
        for driver in drivers:
            ws.append([driver.name, driver.company.name if driver.company else '', 
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
            return redirect('menu')
    else:
        form = CompanyForm()

    return render(request, 'add_company.html', {'form': form})