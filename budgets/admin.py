from django.contrib import admin
from .models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    """Admin interface for Budget model"""
    list_display = ['name', 'user', 'category', 'total_amount', 'remaining_amount', 'spent_percentage', 'created_at']
    list_filter = ['category', 'created_at', 'user']
    search_fields = ['name', 'user__username', 'category']
    ordering = ['-created_at']
    readonly_fields = ['remaining_amount', 'spent_percentage', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'category', 'total_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Calculated Fields', {
            'fields': ('remaining_amount', 'spent_percentage'),
            'classes': ('collapse',)
        }),
    )
