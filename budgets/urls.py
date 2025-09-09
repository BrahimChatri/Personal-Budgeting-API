from django.urls import path
from .views import BudgetListView, BudgetDetailView

app_name = 'budgets'

urlpatterns = [
    path('', BudgetListView.as_view(), name='budget-list'),
    path('<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),
]
