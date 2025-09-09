from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from budgets.models import Budget
from expenses.models import Expense
from decimal import Decimal
from django.utils import timezone
from datetime import date

User = get_user_model()


class ReportsAPITest(APITestCase):
    """Test cases for Reports API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.budget = Budget.objects.create(
            user=self.user,
            name='Monthly Groceries',
            total_amount=Decimal('500.00'),
            category='Food'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_monthly_report_no_data(self):
        """Test monthly report with no expenses"""
        url = reverse('reports:monthly-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary']['total_expenses'], 0.0)
        self.assertEqual(response.data['summary']['total_budget'], 500.0)
        self.assertEqual(response.data['summary']['remaining_budget'], 500.0)
        self.assertEqual(response.data['summary']['spent_percentage'], 0.0)
    
    def test_monthly_report_with_expenses(self):
        """Test monthly report with expenses"""
        # Create expenses for current month
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Grocery shopping',
            amount=Decimal('150.00'),
            date=date(current_year, current_month, 15),
            category='Food'
        )
        
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Restaurant',
            amount=Decimal('75.00'),
            date=date(current_year, current_month, 20),
            category='Food'
        )
        
        url = reverse('reports:monthly-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary']['total_expenses'], 225.0)
        self.assertEqual(response.data['summary']['total_budget'], 500.0)
        self.assertEqual(response.data['summary']['remaining_budget'], 275.0)
        self.assertEqual(response.data['summary']['spent_percentage'], 45.0)
        
        # Check expenses by category
        self.assertEqual(len(response.data['expenses_by_category']), 1)
        self.assertEqual(response.data['expenses_by_category'][0]['category'], 'Food')
        self.assertEqual(response.data['expenses_by_category'][0]['total'], 225.0)
        
        # Check budget vs actual
        self.assertEqual(len(response.data['budget_vs_actual']), 1)
        budget_vs_actual = response.data['budget_vs_actual'][0]
        self.assertEqual(budget_vs_actual['budget_name'], 'Monthly Groceries')
        self.assertEqual(budget_vs_actual['budgeted_amount'], 500.0)
        self.assertEqual(budget_vs_actual['actual_amount'], 225.0)
        self.assertEqual(budget_vs_actual['remaining_amount'], 275.0)
        self.assertEqual(budget_vs_actual['spent_percentage'], 45.0)
    
    def test_monthly_report_specific_month(self):
        """Test monthly report for specific month"""
        # Create expenses for a specific month
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Grocery shopping',
            amount=Decimal('100.00'),
            date=date(2025, 1, 15),
            category='Food'
        )
        
        url = reverse('reports:monthly-report')
        response = self.client.get(url, {'month': 1, 'year': 2025})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['month'], 1)
        self.assertEqual(response.data['year'], 2025)
        self.assertEqual(response.data['summary']['total_expenses'], 100.0)
    
    def test_monthly_report_multiple_categories(self):
        """Test monthly report with multiple categories"""
        # Create another budget and expenses
        transport_budget = Budget.objects.create(
            user=self.user,
            name='Monthly Transport',
            total_amount=Decimal('200.00'),
            category='Transport'
        )
        
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Grocery shopping',
            amount=Decimal('150.00'),
            date=date(current_year, current_month, 15),
            category='Food'
        )
        
        Expense.objects.create(
            budget=transport_budget,
            user=self.user,
            description='Gas station',
            amount=Decimal('50.00'),
            date=date(current_year, current_month, 10),
            category='Transport'
        )
        
        url = reverse('reports:monthly-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary']['total_expenses'], 200.0)
        self.assertEqual(response.data['summary']['total_budget'], 700.0)
        
        # Check expenses by category (should be ordered by total descending)
        self.assertEqual(len(response.data['expenses_by_category']), 2)
        self.assertEqual(response.data['expenses_by_category'][0]['category'], 'Food')
        self.assertEqual(response.data['expenses_by_category'][0]['total'], 150.0)
        self.assertEqual(response.data['expenses_by_category'][1]['category'], 'Transport')
        self.assertEqual(response.data['expenses_by_category'][1]['total'], 50.0)
    
    def test_weekly_report_no_data(self):
        """Test weekly report with no expenses"""
        url = reverse('reports:weekly-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary']['total_expenses'], 0.0)
        self.assertEqual(response.data['summary']['total_budget'], 500.0)
        self.assertEqual(response.data['summary']['remaining_budget'], 500.0)
        self.assertEqual(response.data['summary']['spent_percentage'], 0.0)
    
    def test_weekly_report_with_expenses(self):
        """Test weekly report with expenses"""
        # Create expenses for current week
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Grocery shopping',
            amount=Decimal('75.00'),
            date=start_of_week + timezone.timedelta(days=1),
            category='Food'
        )
        
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Restaurant',
            amount=Decimal('50.00'),
            date=start_of_week + timezone.timedelta(days=3),
            category='Food'
        )
        
        url = reverse('reports:weekly-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary']['total_expenses'], 125.0)
        self.assertEqual(response.data['summary']['total_budget'], 500.0)
        self.assertEqual(response.data['summary']['remaining_budget'], 375.0)
        self.assertEqual(response.data['summary']['spent_percentage'], 25.0)
        
        # Check daily expenses
        self.assertEqual(len(response.data['daily_expenses']), 2)
        
        # Check expenses by category
        self.assertEqual(len(response.data['expenses_by_category']), 1)
        self.assertEqual(response.data['expenses_by_category'][0]['category'], 'Food')
        self.assertEqual(response.data['expenses_by_category'][0]['total'], 125.0)
    
    def test_weekly_report_specific_week(self):
        """Test weekly report for specific week"""
        # Create expenses for a specific week
        specific_date = date(2025, 1, 15)  # A Wednesday
        start_of_week = specific_date - timezone.timedelta(days=specific_date.weekday())
        
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Grocery shopping',
            amount=Decimal('100.00'),
            date=start_of_week + timezone.timedelta(days=1),
            category='Food'
        )
        
        url = reverse('reports:weekly-report')
        response = self.client.get(url, {'weeks_ago': 0})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary']['total_expenses'], 100.0)
    
    def test_reports_require_authentication(self):
        """Test that reports require authentication"""
        self.client.force_authenticate(user=None)
        
        # Test monthly report
        url = reverse('reports:monthly-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test weekly report
        url = reverse('reports:weekly-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_reports_user_isolation(self):
        """Test that users only see their own data in reports"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        other_budget = Budget.objects.create(
            user=other_user,
            name='Other Budget',
            total_amount=Decimal('300.00'),
            category='Food'
        )
        
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        # Create expense for other user
        Expense.objects.create(
            budget=other_budget,
            user=other_user,
            description='Other expense',
            amount=Decimal('100.00'),
            date=date(current_year, current_month, 15),
            category='Food'
        )
        
        # Test monthly report
        url = reverse('reports:monthly-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary']['total_expenses'], 0.0)
        self.assertEqual(response.data['summary']['total_budget'], 500.0)
        
        # Test weekly report
        url = reverse('reports:weekly-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary']['total_expenses'], 0.0)
        self.assertEqual(response.data['summary']['total_budget'], 500.0)
