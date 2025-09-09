from django.db import models
from django.contrib.auth import get_user_model
from budgets.models import Budget

User = get_user_model()


class Expense(models.Model):
    """Expense model for tracking user expenses"""
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'expenses_expense'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.description} - ${self.amount} ({self.date})"
    
    def save(self, *args, **kwargs):
        """Override save to automatically set user from budget"""
        if not self.user_id and self.budget:
            self.user = self.budget.user
        super().save(*args, **kwargs)
