from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta
from expenses.models import Expense
from budgets.models import Budget


class MonthlyReportView(generics.GenericAPIView):
    """View for generating monthly financial reports"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get current month or specified month
        try:
            month = int(request.query_params.get('month', timezone.now().month))
            year = int(request.query_params.get('year', timezone.now().year))
        except (ValueError, TypeError):
            month = timezone.now().month
            year = timezone.now().year
        
        # Calculate date range for the month
        start_date = timezone.datetime(year, month, 1).date()
        if month == 12:
            end_date = timezone.datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            end_date = timezone.datetime(year, month + 1, 1).date() - timedelta(days=1)
        
        # Get user's expenses for the month
        expenses = Expense.objects.filter(
            user=request.user,
            date__range=[start_date, end_date]
        )
        
        # Get user's budgets
        budgets = Budget.objects.filter(user=request.user)
        
        # Calculate totals
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
        total_budget = budgets.aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Expenses by category
        expenses_by_category = expenses.values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        # Budget vs actual by category
        budget_vs_actual = []
        for budget in budgets:
            budget_expenses = expenses.filter(budget=budget)
            actual_amount = budget_expenses.aggregate(total=Sum('amount'))['total'] or 0
            remaining = budget.total_amount - actual_amount
            
            budget_vs_actual.append({
                'budget_name': budget.name,
                'category': budget.category,
                'budgeted_amount': float(budget.total_amount),
                'actual_amount': float(actual_amount),
                'remaining_amount': float(remaining),
                'spent_percentage': float((actual_amount / budget.total_amount) * 100) if budget.total_amount > 0 else 0
            })
        
        return Response({
            'month': month,
            'year': year,
            'period': f"{start_date} to {end_date}",
            'summary': {
                'total_budget': float(total_budget),
                'total_expenses': float(total_expenses),
                'remaining_budget': float(total_budget - total_expenses),
                'spent_percentage': float((total_expenses / total_budget) * 100) if total_budget > 0 else 0
            },
            'expenses_by_category': list(expenses_by_category),
            'budget_vs_actual': budget_vs_actual
        })


class WeeklyReportView(generics.GenericAPIView):
    """View for generating weekly financial reports"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get current week or specified week
        try:
            weeks_ago = int(request.query_params.get('weeks_ago', 0))
        except (ValueError, TypeError):
            weeks_ago = 0
        
        # Calculate date range for the week
        today = timezone.now().date()
        start_date = today - timedelta(days=today.weekday() + (weeks_ago * 7))
        end_date = start_date + timedelta(days=6)
        
        # Get user's expenses for the week
        expenses = Expense.objects.filter(
            user=request.user,
            date__range=[start_date, end_date]
        )
        
        # Get user's budgets
        budgets = Budget.objects.filter(user=request.user)
        
        # Calculate totals
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
        total_budget = budgets.aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Daily expenses breakdown
        daily_expenses = expenses.values('date').annotate(
            total=Sum('amount')
        ).order_by('date')
        
        # Expenses by category for the week
        expenses_by_category = expenses.values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        return Response({
            'week_start': start_date,
            'week_end': end_date,
            'period': f"{start_date} to {end_date}",
            'summary': {
                'total_budget': float(total_budget),
                'total_expenses': float(total_expenses),
                'remaining_budget': float(total_budget - total_expenses),
                'spent_percentage': float((total_expenses / total_budget) * 100) if total_budget > 0 else 0
            },
            'daily_expenses': list(daily_expenses),
            'expenses_by_category': list(expenses_by_category)
        })
