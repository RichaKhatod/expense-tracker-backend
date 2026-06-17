from datetime import date
from django.db.models import Sum
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Expenses, Category
from .serializers import ExpenseSerializer, CategorySerializer


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'source']
    search_fields = ['description']
    ordering_fields = ['date_of_expense', 'amount', 'created_at']
    ordering = ['-date_of_expense']

    def get_queryset(self):
        queryset = Expenses.objects.filter(user=self.request.user)
        month = self.request.query_params.get('month')
        if month:
            year, month_num = map(int, month.split('-'))
            queryset = queryset.filter(
                date_of_expense__year=year,
                date_of_expense__month=month_num,
            )
        return queryset


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expenses.objects.filter(user=self.request.user)


class BulkExpenseCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ExpenseSerializer(
            data=request.data, many=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class MonthlySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        month = request.query_params.get('month')
        if month:
            year, month_num = map(int, month.split('-'))
        else:
            today = date.today()
            year, month_num = today.year, today.month

        expenses = Expenses.objects.filter(
            user=request.user,
            date_of_expense__year=year,
            date_of_expense__month=month_num,
        )
        total = expenses.aggregate(total=Sum('amount'))['total'] or 0
        by_category = list(
            expenses.values('category__category_name')
                    .annotate(total=Sum('amount'))
                    .order_by('-total')
        )
        return Response({
            'year': year,
            'month': month_num,
            'total': total,
            'count': expenses.count(),
            'by_category': by_category,
        })
