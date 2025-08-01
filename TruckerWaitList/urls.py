"""TruckerWaitList URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from waitapp import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('driver_form/', views.driver_form, name='driver_form'),
    path('success/', views.success, name='success'),
    path('queue_list/', views.queue_list, name='queue_list'),
    path('', LoginView.as_view(), name='login'),
    path('menu/', views.menu, name='menu'),
    path('manage_queue/', views.manage_queue, name='manage_queue'),
    path('update_status/', views.update_status, name='update_status'),
    path('report_list/', views.report_list, name='report_list'),
    path('add_company/', views.add_company, name='add_company'),
    path('modify_companies/', views.modify_companies, name='modify_companies'),
    path('edit_company/<int:company_id>/', views.edit_company, name='edit_company'),
    path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),
    path('check_queue_updates/', views.check_queue_updates, name='check_queue_updates'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)