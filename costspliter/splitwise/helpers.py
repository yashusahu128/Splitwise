import json
from django.http import JsonResponse
from .models import Expense, User,Balance
from django.forms.models import model_to_dict
class ApiResponse():

    def send_success(message, data):
        response = {"message": message, 
                    "status": "sucess",
                    "data": data}
        return JsonResponse(response)

    def send_failed(message, data):
        response = {"message": message, 
                    "status": "failed",
                    "data": data}
        return JsonResponse(response)


def update_balances(expense):
    if expense.expense_type == "EQUAL":
        share_per_person = expense.amount / len(expense.participants)
        for participant in expense.participants:
            debtor_payid  = expense.participats_id[participant]
            # if debtor_payid != expense.payer_id:
            Balance.objects.create(debtor_id=debtor_payid,creditor_id=expense.payer_id,amount=share_per_person,expense_id=expense)
                
    elif expense.expense_type == "EXACT":
        total_share = sum(expense.participants.values())
        for participant, share in expense.participants.items():
            debtor_payid  = expense.participats_id[participant]
            # if debtor_payid != expense.payer_id:
            Balance.objects.create(debtor_id=debtor_payid,creditor_id=expense.payer_id,amount=share,expense_id=expense)
                
    elif expense.expense_type == "PERCENT":
        total_percent = sum(expense.participants.values())
        for participant, percent in expense.participants.items():
            # debtor_payid  = expense.participats_id[participant]
            # if debtor_payid != expense.payer_id:
            share = (expense.amount * percent) / total_percent
            share = round(share,2)
            Balance.objects.create(debtor_id=debtor_payid,creditor_id=expense.payer_id,amount=share,expense_id=expense)
                
    return 'expense added'

def queryset_to_list(qs,fields=None, exclude=None):
    return [model_to_dict(x,fields,exclude) for x in qs]

def simplifier(transactions):

    net_balances = {}

    for transaction in transactions:
        debtor = transaction["debtor"]
        creditor = transaction["creditor"]
        amount = transaction["amount"]

        if net_balances.get((creditor, debtor)):
            net_balances[(debtor, creditor)] =abs( net_balances.get((creditor, debtor), 0) - amount)
            net_balances.pop((creditor, debtor))
        else:
            net_balances[(debtor, creditor)] = net_balances.get((debtor, creditor), 0) + amount


    who_owes_whom = {}

 
    for (debtor, creditor), balance in net_balances.items():
        if balance > 0:
            who_owes_whom[(debtor, creditor)] = balance

    final_records = []
    for (debtor, creditor), amount in who_owes_whom.items():
        final_records.append({
                    'creditor':creditor,
                    'debtor'  :debtor,
                    'amount'  :amount,   
        })

    return {'data':final_records}