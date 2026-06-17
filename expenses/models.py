from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	category_name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.category_name

class Expenses(models.Model):
	SOURCE_MANUAL = 'manual'
	SOURCE_SMS = 'sms'
	SOURCE_CHOICES = [(SOURCE_MANUAL, 'Manual'), (SOURCE_SMS, 'SMS')]

	amount = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField(blank=True, null=True)
	date_of_expense = models.DateField(blank=True, null=True)
	source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default=SOURCE_MANUAL)
	raw_sms = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = "Expenses"

	def __str__(self):
		return f"{self.user} - {self.amount} - {self.date_of_expense}"