from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from budgets.models import Budget
from .models import Expense
from decimal import Decimal
from django.utils import timezone

User = get_user_model()


class ExpenseModelTest(TestCase):
    """Test cases for Expense model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.budget = Budget.objects.create(
            user=self.user,
            name='Test Budget',
            total_amount=Decimal('1000.00'),
            category='Food'
        )
        self.expense = Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Grocery shopping',
            amount=Decimal('75.50'),
            date='2025-01-15',
            category='Food'
        )
    
    def test_expense_creation(self):
        """Test creating an expense"""
        self.assertEqual(self.expense.description, 'Grocery shopping')
        self.assertEqual(self.expense.amount, Decimal('75.50'))
        self.assertEqual(self.expense.category, 'Food')
        self.assertEqual(self.expense.budget, self.budget)
        self.assertEqual(self.expense.user, self.user)
    
    def test_expense_auto_user_assignment(self):
        """Test that user is automatically assigned from budget"""
        new_expense = Expense(
            budget=self.budget,
            description='Test expense',
            amount=Decimal('50.00'),
            date='2025-01-16',
            category='Food'
        )
        new_expense.save()
        
        self.assertEqual(new_expense.user, self.user)
    
    def test_expense_string_representation(self):
        """Test expense string representation"""
        expected = "Grocery shopping - $75.50 (2025-01-15)"
        self.assertEqual(str(self.expense), expected)


class ExpenseAPITest(APITestCase):
    """Test cases for Expense API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.budget = Budget.objects.create(
            user=self.user,
            name='Test Budget',
            total_amount=Decimal('1000.00'),
            category='Food'
        )
        self.client.force_authenticate(user=self.user)
        self.expense_data = {
            'budget_id': self.budget.id,
            'description': 'Grocery shopping',
            'amount': '75.50',
            'date': '2025-01-15',
            'category': 'Food'
        }
    
    def test_create_expense(self):
        """Test creating a new expense"""
        url = reverse('expenses:expense-list')
        response = self.client.post(url, self.expense_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], 'Grocery shopping')
        self.assertEqual(response.data['amount'], '75.50')
        self.assertEqual(response.data['user'], 'testuser')
    
    def test_create_expense_invalid_amount(self):
        """Test creating expense with invalid amount"""
        url = reverse('expenses:expense-list')
        invalid_data = self.expense_data.copy()
        invalid_data['amount'] = '-50.00'
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_expense_future_date(self):
        """Test creating expense with future date"""
        url = reverse('expenses:expense-list')
        future_date = (timezone.now().date() + timezone.timedelta(days=1)).strftime('%Y-%m-%d')
        invalid_data = self.expense_data.copy()
        invalid_data['date'] = future_date
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_expenses(self):
        """Test listing user expenses"""
        # Create an expense
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Test expense',
            amount=Decimal('50.00'),
            date='2025-01-15',
            category='Food'
        )
        
        url = reverse('expenses:expense-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['description'], 'Test expense')
    
    def test_list_expenses_user_isolation(self):
        """Test that users only see their own expenses"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        other_budget = Budget.objects.create(
            user=other_user,
            name='Other Budget',
            total_amount=Decimal('1000.00'),
            category='Food'
        )
        
        # Create expense for other user
        Expense.objects.create(
            budget=other_budget,
            user=other_user,
            description='Other expense',
            amount=Decimal('50.00'),
            date='2025-01-15',
            category='Food'
        )
        
        url = reverse('expenses:expense-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_filter_expenses_by_category(self):
        """Test filtering expenses by category"""
        # Create expenses with different categories
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Food expense',
            amount=Decimal('50.00'),
            date='2025-01-15',
            category='Food'
        )
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Transport expense',
            amount=Decimal('30.00'),
            date='2025-01-15',
            category='Transport'
        )
        
        url = reverse('expenses:expense-list')
        response = self.client.get(url, {'category': 'Food'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['category'], 'Food')
    
    def test_search_expenses(self):
        """Test searching expenses by description"""
        # Create expenses with different descriptions
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Grocery shopping',
            amount=Decimal('50.00'),
            date='2025-01-15',
            category='Food'
        )
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Gas station',
            amount=Decimal('30.00'),
            date='2025-01-15',
            category='Transport'
        )
        
        url = reverse('expenses:expense-list')
        response = self.client.get(url, {'search': 'grocery'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('grocery', response.data['results'][0]['description'].lower())
    
    def test_retrieve_expense(self):
        """Test retrieving a specific expense"""
        expense = Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Test expense',
            amount=Decimal('50.00'),
            date='2025-01-15',
            category='Food'
        )
        
        url = reverse('expenses:expense-detail', kwargs={'pk': expense.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Test expense')
        self.assertEqual(response.data['amount'], '50.00')
    
    def test_update_expense(self):
        """Test updating an expense"""
        expense = Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Test expense',
            amount=Decimal('50.00'),
            date='2025-01-15',
            category='Food'
        )
        
        url = reverse('expenses:expense-detail', kwargs={'pk': expense.pk})
        update_data = {
            'budget_id': self.budget.id,
            'description': 'Updated expense',
            'amount': '75.00',
            'date': '2025-01-16',
            'category': 'Groceries'
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Updated expense')
        self.assertEqual(response.data['amount'], '75.00')
    
    def test_delete_expense(self):
        """Test deleting an expense"""
        expense = Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Test expense',
            amount=Decimal('50.00'),
            date='2025-01-15',
            category='Food'
        )
        
        url = reverse('expenses:expense-detail', kwargs={'pk': expense.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(pk=expense.pk).exists())
    
    def test_expense_requires_authentication(self):
        """Test that expense access requires authentication"""
        self.client.force_authenticate(user=None)
        url = reverse('expenses:expense-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
