from json.encoder import JSONEncoder
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, QueryDict
from http import HTTPStatus
from .models import Customer, Deposit, Wallet, Withdraw
import uuid
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import datetime
import json

# Create your views here.
'''
- Initialize my account for wallet
- Enable Wallet
- View My Wallet balance
- Add virtual money to my wallet
- Use virtual money from my wallet
- Disable wallet
'''
user_customer = None
def index(request):
    # return HttpResponse('<h1>Hey, Welcome! </h1>')
    return render(request, 'index.html')

@csrf_protect
def start(request):
    return render(request,'start.html')

def register(request):
    if request.method == "POST":
        id = uuid.uuid4()
        words = request.POST['words']
        context = {
            'name': words,
            'id': id
        }
        if Customer.objects.filter(name=words).exists():
            messages.info(request,'Name already exists')
            return redirect('index')
        else:
            customer = Customer.objects.create(id=id, name=words)
            customer.save()
            customer_saved = Customer.objects.get(id=id)
            user_customer = customer_saved
            return redirect('start')
    else:
        Wallet.objects.all().delete()
        Customer.objects.all().delete()
        return redirect('index')
@csrf_exempt
def withdrawals(request): 
    wallet = Wallet.objects.last() 
    headers = request.headers
    author = headers['Authorization']
    token = author.split(' ')[1]
    if token is None or token == '' or token != 'cb04f9f26632ad602f14acef21c58f58f6fe5fb55a':
        return JsonResponse({'data': 'token not correct'})
    amount = request.POST['amount']
    ref_id = request.POST['reference_id']
    amount = float (amount)
    wd_id = uuid.uuid4()
    wd_make = Withdraw.objects.create(id=wd_id, from_wallet= wallet, withdrawn_by= wallet.owned_by, amount= amount, reference_id = ref_id )
    wd_make.save()
    
    wallet.balance_amount = wallet.balance_amount - amount
    wallet.save()
    data = {
    "status": "success",
    "data": {
        "withdrawal": {
            "id": wd_id,
            "withdrawn_by": wallet.owned_by.id,
            "status": "success",
            "withdrawn_at": wd_make.withdrawn_at.strftime("%Y-%m-%d %H:%M:%S"),
            "amount": amount,
                "reference_id": ref_id
            }
        }
    }
    return JsonResponse (data)

@csrf_exempt
def deposits(request): 
    wallet = Wallet.objects.last() 
    headers = request.headers
    author = headers['Authorization']
    token = author.split(' ')[1]
    if token is None or token == '' or token != 'cb04f9f26632ad602f14acef21c58f58f6fe5fb55a':
        return JsonResponse({'data': 'token not correct'})
    amount = request.POST['amount']
    ref_id = request.POST['reference_id']
    amount = float(amount)
    depo_id = uuid.uuid4()
    deposit_make = Deposit.objects.create(id=depo_id, for_wallet= wallet, deposited_by= wallet.owned_by, amount= amount, reference_id = ref_id )
    deposit_make.save()
    wallet.balance_amount = wallet.balance_amount + amount
    wallet.save()
    deposit_made = Deposit.objects.get(id=depo_id)
    data = {
        "status": "success",
        "data": {
            "deposit": {
                "id": depo_id,
                "deposited_by": wallet.owned_by.id,
                "status": "success",
                "deposited_at": deposit_made.deposited_at.strftime("%Y-%m-%d %H:%M:%S"),
                "amount": amount,
                "reference_id": ref_id
            }
        }
    }
    return JsonResponse (data)

@csrf_exempt
def wallet(request): 
    wallet = Wallet.objects.last() 
    headers = request.headers
    author = headers['Authorization']
    token = author.split(' ')[1]
    if token is None or token == '' or token != 'cb04f9f26632ad602f14acef21c58f58f6fe5fb55a':
        return JsonResponse({'data': 'token not correct'})
    if request.method == 'POST':
        if wallet.enabled == True:
            data = {
                "status": "fail",
                "data": {
                    "error": "Already enabled" 
                }
            }
            return JsonResponse (data, status=HTTPStatus.BAD_REQUEST)
        else:
            wallet.enabled = True
            wallet.enabled_at = datetime.now()
            wallet.save()
            succes_data = {
                "status": "success",
                "data": {
                    "wallet": {
                        "id": wallet.id,
                        "owned_by":wallet.owned_by.id,
                        "status": "enabled",
                        "enabled_at": wallet.enabled_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "balance": wallet.balance_amount
                    }
                }
            }
            return JsonResponse (succes_data)
    elif request.method == 'GET':
        if wallet.enabled != True:
            data = {
                "status": "fail",
                "data": {
                    "error": "Disabled"
                }
            }
            return JsonResponse(data, status=HTTPStatus.NOT_FOUND)
        else:
            success_data = {
            "status": "success",
            "data": {
                "wallet": {
                    "id": wallet.id,
                    "owned_by": wallet.owned_by.id,
                    "status": "enabled",
                    "enabled_at": wallet.enabled_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "balance": wallet.balance_amount
                    }
                }
            }
            return JsonResponse(success_data)
    elif request.method == 'PATCH':
        data = QueryDict(request.body)
        name = data[' name']
        splitted_data = name.splitlines()
        is_disabled = splitted_data[2]
        if is_disabled.lower() == 'true':
            wallet.enabled = False
            wallet.disabled_at = datetime.now()
            wallet.save()
            data = {
            "status": "success",
            "data": {
                "wallet": {
                    "id": wallet.id,
                    "owned_by": wallet.owned_by.id,
                    "status": "disabled",
                    "disabled_at": wallet.disabled_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "balance": wallet.balance_amount
                }
            }
            }
            return JsonResponse(data)
    
# @csrf_protect
@csrf_exempt
def init(request):  
    data = {
            "error": {
            "customer_xid": [
                "Missing data for required field."
            ]
        }
        }
    res = {
            'data' : data,
            'status': 'fail'
            
            
        }
    if 'customer_xid' not in request.POST:
        return JsonResponse(res, status=HTTPStatus.BAD_REQUEST)
    cust_id = request.POST['customer_xid']
    if cust_id is None or cust_id == '':
        return JsonResponse(res, status=HTTPStatus.BAD_REQUEST)  
    wallet_uuid = uuid.uuid4()
    customer = Customer.objects.get(id=cust_id)
    last_wallet = Wallet.objects.last()

    wallet_no = 1
    if last_wallet:
        wallet_no = last_wallet + last_wallet.wallet_no
    wallet = Wallet.objects.create(id=wallet_uuid, owned_by=customer, wallet_no = wallet_no,balance_amount=0.0)
    wallet.save()
    success=    {
    "data": {
        "token": "cb04f9f26632ad602f14acef21c58f58f6fe5fb55a"
    },
    "status": "success"
    }
    
    return JsonResponse(success)