from django import forms
from .models import User, Expense

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        feilds = ('name','mobile','email')
        exclude = ["user_id"]

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        feilds = ('payer_id','amount','expense_type', 'expense_name', 'notes', 'images' )
        exclude = ["expense_id","participants"]