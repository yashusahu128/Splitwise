from django.urls import path
from .apps import SplitwiseConfig
from .views import UserCreate, AddExpense, ShowBalance, ShowExpenses
urlpatterns = [
    path("user", UserCreate.as_view()),
    path("add_expense", AddExpense.as_view()),
    path("show_records", ShowBalance.as_view()),
    path("show_expenses/<user_id>", ShowExpenses.as_view()),
    # path("show_records/<user_id>", AddExpense.as_view()),
]
