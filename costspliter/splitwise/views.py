
from django.views.generic import View
from django.http import JsonResponse
import json
from .forms import UserForm, ExpenseForm
from .models import User, Expense, Balance
from .helpers import ApiResponse, update_balances, queryset_to_list, simplifier
import copy



class UserCreate(View):
    
    def post(self,request):
        data = json.loads(request.body)
        form = UserForm(data)
        
        if form.is_valid():
            user = User.objects.create(**data)
            return ApiResponse.send_success(data= data,message='user added')
        form.is_valid
        error = dict(form.errors)
        return ApiResponse.send_failed(data=error,message='')

class AddExpense(View):
    def get_user(self,payer_id):
        user = User.objects.get(email= payer_id)
        return user
        
    def post(self,request):
        data = json.loads(request.body)
        respose_data = copy.deepcopy(data)
        
        user_id = self.get_user(data["payer_id"])
        data['payer_id'] = user_id
        participants = data.pop('participants')
        form = ExpenseForm(data)
        if form.is_valid():
            
            expense = Expense.objects.create(**data)

            expense.participants = participants
            expense.participats_id = {pi:self.get_user(pi) for pi in participants.keys()}

            
        
            if (expense.expense_type == 'PERCENT'  and sum(expense.participants.values()) == 100 )or \
                (expense.expense_type == 'EXACT'  and sum(expense.participants.values()) == expense.amount)\
              or (expense.expense_type == 'EQUAL'):
                
                update_balances(expense=expense)
                
                return ApiResponse.send_success(data= respose_data,message='expense added')
            
            message = 'Total Amount is not equal as per participants shares'
        
        
        error = dict(form.errors)
        return ApiResponse.send_failed(data=error,message=message)

class ShowBalance(View):

    def get_user(self,pid):
        user = User.objects.get(email= pid)
        return user
    
    def get(self,request):
        parameters = request.GET.dict()
        balance_data = Balance.objects.all()
        balance_data=queryset_to_list(balance_data)
        

        #retrieving userids
        user_data = User.objects.all()        
        user_data=queryset_to_list(user_data)
        user_dict = {info['user_id']:info['name'] for info in user_data}
        
        balance_info = []
        for bd in balance_data:
            if user_dict[bd['creditor_id']] == user_dict[bd['debtor_id']]:
                continue
            balance_info.append(
                {
                    'creditor':user_dict[bd['creditor_id']],
                    'debtor'  :user_dict[bd['debtor_id']],
                    'amount'  :bd['amount'],
                }
            )
        
        if parameters.get('Simplify','false') == 'true' :
            

            balance_info = simplifier(balance_info)
        else:
            balance_info = {'data':balance_info}


        return JsonResponse(balance_info)

class ShowExpenses(View):
    def get_user(self,pid):
        user = User.objects.get(email= pid)
        return user
    
    def get_expnese_obj(self,pid):
        exp_obj = Expense.objects.get(expense_id= pid)
        return exp_obj
    

    def get(self,request,**kwargs):
        user = kwargs.get('user_id')
        user = self.get_user(user)
        user_id = user.user_id
        my_expenses_info = Balance.objects.all()
    
        my_expenses_info=queryset_to_list(my_expenses_info)

        balance_info = {'user_expense':{},"Overall_Debt":{}}
        for ped in my_expenses_info:
            if ped['expense_id']:
                expnse_name = self.get_expnese_obj(ped['expense_id']).expense_name
                if ped['debtor_id'] == user_id and ped['creditor_id'] == user_id:
                    balance_info['user_expense'][expnse_name] = balance_info['user_expense'].get(expnse_name,0)+ped['amount']
                
                elif ped['debtor_id'] == user_id and ped['creditor_id'] != user_id:
                    balance_info['Overall_Debt'][expnse_name] = balance_info['Overall_Debt'].get(expnse_name,0)+ped['amount']


        return JsonResponse(balance_info)


        


        
    

    

    
    

        

        



        


        






