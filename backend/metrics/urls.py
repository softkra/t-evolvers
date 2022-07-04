"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from .views import MetricList, MetricDetails, NotificationsApiView, DashboardApiView, CSVReport, ExcelReport

urlpatterns = [
    path('', MetricList.as_view()),
    path('<int:pk>/', MetricDetails.as_view()),
    path('notifications/', NotificationsApiView.as_view()),
    path('dashboard/', DashboardApiView.as_view()),
    path('generate_csv/', CSVReport),
    path('generate_excel/', ExcelReport),
]
