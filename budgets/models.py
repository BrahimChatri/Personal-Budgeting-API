from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Budget(models.Model):
    """Budget model for managing user budgets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'budgets_budget'
        ordering = ['-created_at']
        unique_together = ['user', 'name', 'category']
    
    def __str__(self):
        return f"{self.name} - {self.category} (${self.total_amount})"
    
    @property
    def remaining_amount(self):
        """Calculate remaining budget amount"""
        total_expenses = sum(expense.amount for expense in self.expenses.all())
        return self.total_amount - total_expenses
    
    @property
    def spent_percentage(self):
        """Calculate percentage of budget spent"""
        if self.total_amount == 0:
            return 0
        total_expenses = sum(expense.amount for expense in self.expenses.all())
        return (total_expenses / self.total_amount) * 100
