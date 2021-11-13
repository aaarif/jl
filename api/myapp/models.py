from django.db import models
import uuid
from datetime import datetime
from django.utils import timezone
# Create your models here.
'''
- customer: id, name
- Wallet: cust_id, wallet_no, balance_amount
- wallet: wallet_idvirtual_money
'''
class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owned_by = models.ForeignKey(Customer, on_delete=models.PROTECT)
    wallet_no = models.IntegerField()
    balance_amount = models.FloatField() 
    initialized_at = models.DateTimeField(default=timezone.now())
    enabled = models.BooleanField(default=False)
    enabled_at = models.DateTimeField(null=True)
    disabled_at = models.DateTimeField(null=True)
    
class Deposit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    for_wallet = models.ForeignKey(Wallet,on_delete=models.PROTECT)
    deposited_by = models.ForeignKey(Customer,on_delete=models.PROTECT)
    amount = models.FloatField() 
    deposited_at = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100)

class Withdraw(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_wallet = models.ForeignKey(Wallet,on_delete=models.PROTECT)
    withdrawn_by = models.ForeignKey(Customer,on_delete=models.PROTECT)
    amount = models.FloatField() 
    withdrawn_at = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100)
    
    