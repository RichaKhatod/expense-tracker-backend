from django.urls import path
from expenses import views

urlpatterns = [
    path('expenses/', views.ExpenseListCreateView.as_view(), name='expense-list'),
    path('expenses/bulk/', views.BulkExpenseCreateView.as_view(), name='expense-bulk'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense-detail'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('summary/', views.MonthlySummaryView.as_view(), name='monthly-summary'),
]