from django.urls import path
from .views import ExpenseListView, ExpenseDetailView

app_name = 'expenses'

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expense-list'),
    path('<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
]
