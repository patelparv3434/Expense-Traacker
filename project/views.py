from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import Addfunds , Expense

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        repeatpassword = request.POST.get("repeatpassword")

        if password == repeatpassword:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('register')

    return render(request, "register.html")


def Login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        lpassword = request.POST.get("lpassword")

        user = authenticate(request , username = username , password = lpassword)
        if user is not None:
            login(request  , user)
            return redirect('home')
        else:
            messages.error(request , "not valid email or password")
    return render(request , "login.html")

def Logout(request):
    logout(request)
    return redirect('login')

@login_required()
def home(request):
    context = {}
    if request.method == "POST":
         # add fund section
        if "addfund_submit" in request.POST:
            addfunds = request.POST.get("addfunds")

            if addfunds and addfunds.strip():
                Addfunds.objects.create(Add = addfunds , user=request.user)
                return redirect('home')
       

        # reason and amount for expenses section
        elif "expense_submit" in request.POST:
            reason = request.POST.get("reason")
            amount = request.POST.get("amount")
            date = request.POST.get("date")

            if reason and amount and amount.strip():
                if date:
                    date = parse_datetime(date)
                else:
                    date = timezone.now()
                Expense.objects.create(Reason = reason , Amount = int(amount) , Date = date ,  user=request.user)
                return redirect('home')

    show_expense = Expense.objects.filter(user=request.user).order_by('-Date')



         # current balance 

    total_funds = Addfunds.objects.filter(
            user = request.user
        ).aggregate(Sum('Add'))['Add__sum'] or 0

    total_expense = Expense.objects.filter(
            user = request.user
        ).aggregate(Sum("Amount"))['Amount__sum'] or 0

    current_balance = total_funds - total_expense

    context = {
                'current_balance' : current_balance , 
                'show_expense' : show_expense
        }


            
    return render(request , "home.html" , context)


def track(request):
    return render(request , "track.html")