from django.urls import path
from .views import MonthlyReportView, WeeklyReportView

app_name = 'reports'

urlpatterns = [
    path('monthly/', MonthlyReportView.as_view(), name='monthly-report'),
    path('weekly/', WeeklyReportView.as_view(), name='weekly-report'),
]
