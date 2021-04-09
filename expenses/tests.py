from django.test import TestCase
from django.utils import timezone
from django.db import models
from django.urls import reverse
import datetime

from .models import Expense


def create_expense_in_future():
    time_30_after = timezone.now() + datetime.timedelta(days=0)
    expense_id = models.AutoField(primary_key=True)
    return Expense(expense_id, time_30_after, 4, 23.23)


class ExpenseModelTests(TestCase):

    def test_new_expense_added_is_in_future(self):
        future_expense = create_expense_in_future()
        self.assertIs(future_expense.purchase_date_valid(), False)


class NewExpenseTests(TestCase):
    def test_new_expense_added_is_in_future(self):
        pass
