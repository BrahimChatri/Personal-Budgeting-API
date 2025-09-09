from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Budget
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
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
