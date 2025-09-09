from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Admin interface for Expense model"""
    list_display = ['description', 'user', 'budget', 'category', 'amount', 'date', 'created_at']
    list_filter = ['category', 'date', 'created_at', 'user', 'budget']
    search_fields = ['description', 'user__username', 'budget__name', 'category']
    ordering = ['-date', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'budget', 'description', 'amount', 'category', 'date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user', 'budget')
