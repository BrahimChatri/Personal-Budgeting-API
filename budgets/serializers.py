from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for Budget model"""
    remaining_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    spent_percentage = serializers.FloatField(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Budget
        fields = [
            'id', 'user', 'name', 'total_amount', 'category', 
            'created_at', 'updated_at', 'remaining_amount', 'spent_percentage'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class BudgetCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating budgets"""
    
    class Meta:
        model = Budget
        fields = ['name', 'total_amount', 'category']
    
    def validate_total_amount(self, value):
        """Validate that total_amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Total amount must be greater than zero")
        return value
