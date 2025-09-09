from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Expense
from .serializers import ExpenseSerializer, ExpenseCreateSerializer
from budgets.models import Budget


class ExpenseListView(generics.ListCreateAPIView):
    """View for listing and creating expenses"""
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'date', 'budget']
    search_fields = ['description', 'category']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExpenseCreateSerializer
        return ExpenseSerializer
    
    def perform_create(self, serializer):
        budget_id = serializer.validated_data['budget_id']
        budget = Budget.objects.get(id=budget_id)
        serializer.save(user=self.request.user, budget=budget)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting expenses"""
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ExpenseCreateSerializer
        return ExpenseSerializer
    
    def perform_update(self, serializer):
        if 'budget_id' in serializer.validated_data:
            budget_id = serializer.validated_data['budget_id']
            budget = Budget.objects.get(id=budget_id)
            serializer.save(budget=budget)
        else:
            serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        expense = self.get_object()
        expense.delete()
        return Response(
            {'message': 'Expense deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )
