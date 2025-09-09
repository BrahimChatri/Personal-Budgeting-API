from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Budget
from expenses.models import Expense
from decimal import Decimal

User = get_user_model()


class BudgetModelTest(TestCase):
    """Test cases for Budget model"""
    
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
    
    def test_budget_creation(self):
        """Test creating a budget"""
        self.assertEqual(self.budget.name, 'Test Budget')
        self.assertEqual(self.budget.total_amount, Decimal('1000.00'))
        self.assertEqual(self.budget.category, 'Food')
        self.assertEqual(self.budget.user, self.user)
    
    def test_remaining_amount_calculation(self):
        """Test remaining amount calculation"""
        # Create an expense
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Grocery shopping',
            amount=Decimal('250.00'),
            date='2025-01-15',
            category='Food'
        )
        
        self.assertEqual(self.budget.remaining_amount, Decimal('750.00'))
    
    def test_spent_percentage_calculation(self):
        """Test spent percentage calculation"""
        # Create an expense
        Expense.objects.create(
            budget=self.budget,
            user=self.user,
            description='Grocery shopping',
            amount=Decimal('250.00'),
            date='2025-01-15',
            category='Food'
        )
        
        self.assertEqual(self.budget.spent_percentage, 25.0)
    
    def test_spent_percentage_zero_budget(self):
        """Test spent percentage with zero budget"""
        zero_budget = Budget.objects.create(
            user=self.user,
            name='Zero Budget',
            total_amount=Decimal('0.00'),
            category='Test'
        )
        
        self.assertEqual(zero_budget.spent_percentage, 0)
    
    def test_budget_string_representation(self):
        """Test budget string representation"""
        expected = "Test Budget - Food ($1000.00)"
        self.assertEqual(str(self.budget), expected)


class BudgetAPITest(APITestCase):
    """Test cases for Budget API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.budget_data = {
            'name': 'Monthly Groceries',
            'total_amount': '500.00',
            'category': 'Food'
        }
    
    def test_create_budget(self):
        """Test creating a new budget"""
        url = reverse('budgets:budget-list')
        response = self.client.post(url, self.budget_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Monthly Groceries')
        self.assertEqual(response.data['total_amount'], '500.00')
        self.assertEqual(response.data['user'], 'testuser')
    
    def test_create_budget_invalid_amount(self):
        """Test creating budget with invalid amount"""
        url = reverse('budgets:budget-list')
        invalid_data = self.budget_data.copy()
        invalid_data['total_amount'] = '-100.00'
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_budgets(self):
        """Test listing user budgets"""
        # Create a budget
        Budget.objects.create(
            user=self.user,
            name='Test Budget',
            total_amount=Decimal('1000.00'),
            category='Food'
        )
        
        url = reverse('budgets:budget-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Budget')
    
    def test_list_budgets_user_isolation(self):
        """Test that users only see their own budgets"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        # Create budget for other user
        Budget.objects.create(
            user=other_user,
            name='Other Budget',
            total_amount=Decimal('1000.00'),
            category='Food'
        )
        
        url = reverse('budgets:budget-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_retrieve_budget(self):
        """Test retrieving a specific budget"""
        budget = Budget.objects.create(
            user=self.user,
            name='Test Budget',
            total_amount=Decimal('1000.00'),
            category='Food'
        )
        
        url = reverse('budgets:budget-detail', kwargs={'pk': budget.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Budget')
        self.assertEqual(response.data['remaining_amount'], '1000.00')
        self.assertEqual(response.data['spent_percentage'], 0.0)
    
    def test_update_budget(self):
        """Test updating a budget"""
        budget = Budget.objects.create(
            user=self.user,
            name='Test Budget',
            total_amount=Decimal('1000.00'),
            category='Food'
        )
        
        url = reverse('budgets:budget-detail', kwargs={'pk': budget.pk})
        update_data = {
            'name': 'Updated Budget',
            'total_amount': '750.00',
            'category': 'Groceries'
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Budget')
        self.assertEqual(response.data['total_amount'], '750.00')
    
    def test_delete_budget(self):
        """Test deleting a budget"""
        budget = Budget.objects.create(
            user=self.user,
            name='Test Budget',
            total_amount=Decimal('1000.00'),
            category='Food'
        )
        
        url = reverse('budgets:budget-detail', kwargs={'pk': budget.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Budget.objects.filter(pk=budget.pk).exists())
    
    def test_budget_requires_authentication(self):
        """Test that budget access requires authentication"""
        self.client.force_authenticate(user=None)
        url = reverse('budgets:budget-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
