from django.db import models





# Define User, Expense, and Balance models
class User(models.Model):
   
    user_id = models.AutoField(primary_key=True)
    name = models.CharField()
    email = models.EmailField()
    mobile = models.IntegerField()


class Expense(models.Model):

    expense_id = models.AutoField(primary_key=True)
    payer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    expense_type = models.CharField()
    expense_name = models.CharField()
    notes = models.CharField(null=True, blank=True)
    images = models.CharField(null=True, blank=True)


class Balance(models.Model):
    
    balance_id = models.AutoField(primary_key=True)
    debtor_id = models.ForeignKey(User, related_name= "u1", on_delete=models.CASCADE)
    creditor_id = models.ForeignKey(User, related_name= "u2",on_delete=models.CASCADE)
    amount = models.FloatField()
    expense_id = models.ForeignKey(Expense,null=True,on_delete=models.CASCADE)
    







