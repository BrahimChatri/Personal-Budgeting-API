from rest_framework import serializers
from .models import Expense
from budgets.models import Budget


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense model"""
    budget_name = serializers.CharField(source='budget.name', read_only=True)
    budget_category = serializers.CharField(source='budget.category', read_only=True)
    budget_id = serializers.IntegerField(write_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Expense
        fields = [
            'id', 'budget_name', 'budget_category', 'budget_id', 'user', 'description', 'amount', 
            'date', 'category', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'budget_name', 'budget_category', 'user', 'created_at', 'updated_at']


class ExpenseCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating expenses"""
    budget_id = serializers.PrimaryKeyRelatedField(
        source='budget',
        queryset=Budget.objects.all(),
        write_only=True,
        error_messages={
            'does_not_exist': 'Budget does not exist',
            'incorrect_type': 'Invalid budget id',
            'invalid': 'Invalid budget id',
            'required': 'budget_id is required'
        }
    )
    
    class Meta:
        model = Expense
        fields = ['budget_id', 'description', 'amount', 'date', 'category']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            self.fields['budget_id'].queryset = Budget.objects.filter(user=request.user)
    
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
    
    # No need for validate_budget_id; queryset restriction handles existence/ownership
