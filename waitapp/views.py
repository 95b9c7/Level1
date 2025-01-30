from django.shortcuts import render, redirect, HttpResponse, get_list_or_404, get_object_or_404
from .forms import TruckDriverForm, MasterReportForm
from .models import TruckDriver
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
import os
from django.utils import timezone
import openpyxl
from openpyxl import Workbook


# Create your views here.
def driver_form(request):
    if request.method == 'POST':
        form = TruckDriverForm(request.POST)
        if form.is_valid():
            # Do something with the form data, e.g., save it to the database
            form.save()

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

@login_required
def update_status(request):
    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        new_status = request.POST.get('new_status')

        try:
            submission = get_object_or_404(TruckDriver, id=submission_id)

            if new_status == 'In Progress' and submission.status != 'In Progress':
                submission.status = 'In Progress'
                submission.in_progress_time = datetime.now().time()
                submission.in_progress_date = datetime.now().date()
                submission.in_progress_employee = request.user.username  # Set the user who changed it to 'In Progress'
                
            elif new_status == 'Finished' and submission.status != 'Finished':
                submission.status = 'Finished'
                submission.finished_time = datetime.now().time()
                submission.finished_date = datetime.now().date()
                submission.finished_employee = request.user.username  # Set the user who changed it to 'Finished'
                
            submission.save()
            return JsonResponse({'success': True})
        except TruckDriver.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Submission not found'})
        
    return JsonResponse({'success': False, 'error': 'Invalid request'})


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

        ws.append(['Name', 'DOT Number', 'Company', 'Status', 'Check In Time', 
                    'Check In Date', 'In Progress Time', 'In Progress Date', 'In Progress Employee',
                    'Finished Time', 'Finished Date', 'Finished Employee'])
        for driver in drivers:
            ws.append([driver.name, driver.dot_number, driver.company, 
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