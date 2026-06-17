from django.contrib import admin
from expenses.models import Category, Expenses

admin.site.register(Category)
# admin.site.register(Expenses)

@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'category', 'date_of_expense']

    list_filter = ['user', 'category', 'date_of_expense']

    search_fields = ['description', 'user__username']

    ordering = ['-created_at']