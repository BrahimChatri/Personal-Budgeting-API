from rest_framework import serializers
from .models import Expense
from budgets.serializers import BudgetSerializer


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense model"""
    budget = BudgetSerializer(read_only=True)
    budget_id = serializers.IntegerField(write_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Expense
        fields = [
            'id', 'budget', 'budget_id', 'user', 'description', 'amount', 
            'date', 'category', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'budget', 'user', 'created_at', 'updated_at']


class ExpenseCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating expenses"""
    
    class Meta:
        model = Expense
        fields = ['budget_id', 'description', 'amount', 'date', 'category']
    
    def validate_amount(self, value):
        """Validate that amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value
    
    def validate_date(self, value):
        """Validate that date is not in the future"""
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future")
        return value
    
    def validate_budget_id(self, value):
        """Validate that budget exists and belongs to user"""
        from budgets.models import Budget
        try:
            budget = Budget.objects.get(id=value)
            if budget.user != self.context['request'].user:
                raise serializers.ValidationError("Budget does not belong to you")
        except Budget.DoesNotExist:
            raise serializers.ValidationError("Budget does not exist")
        return value
