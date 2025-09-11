from django.shortcuts import render
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from rest_framework import status
from .models import Budget
from django.db import IntegrityError
from .serializers import BudgetSerializer, BudgetCreateSerializer


# Create your views here.


class BudgetListView(generics.ListCreateAPIView):
    """View for listing and creating budgets"""
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BudgetCreateSerializer
        return BudgetSerializer
    
    def create(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            instance = input_serializer.save(user=request.user)
        except IntegrityError:
            raise serializers.ValidationError({
                'non_field_errors': ['A budget with this name and category already exists.']
            })

        output_serializer = BudgetSerializer(instance)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting budgets"""
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BudgetCreateSerializer
        return BudgetSerializer
    
    def destroy(self, request, *args, **kwargs):
        budget = self.get_object()
        budget.delete()
        return Response(
            {'message': 'Budget deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )
