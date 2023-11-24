from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from .models import Myexpense
from django.db import models
from .forms import AddExpenseForm,NewUserform
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'myexpense/home.html')

def Register(request):
    if request.method == "POST":
        form = NewUserform(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"User registerd successflly...")
            return redirect('/login')
    else:
        form = NewUserform()
    return render(request,'account/register.html',{'form':form})


def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username,password = password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("list/")
            else:
                
                messages.error(request,"Please Enter  valid creditails ") 
                return redirect("register/")  
        else:
            messages.error(request,"Invalid username or password.")

    else:
        form = AuthenticationForm()
    return render(request,'account/login.html',{'form':form})


@login_required(login_url='/login')
def Logout(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('home')

@login_required(login_url='/login')
def Profit_list(request):
    profit_list= Myexpense.objects.filter(user = request.user) 
    total_amount = profit_list.aggregate(models.Sum("ProfitAmount"))["ProfitAmount__sum"] or 0
    return render(request,"myexpense/list.html",{"profit_list":profit_list, "total_amount":total_amount})

@login_required(login_url='/login')
def AddExpense(request):
    if request.method == "POST":
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            form.save()
            return redirect('/list/')
    else:
        form= AddExpenseForm()
    return render(request,'myexpense/add.html',{'form':form}) 


@login_required(login_url='/login')
def Search(request):
    profit_list= Myexpense.objects.filter(user = request.user)
    query = request.GET['query']
    lists = profit_list.filter(Expensename__icontains = query)
    total_amount = lists.aggregate(models.Sum("ProfitAmount"))["ProfitAmount__sum"] or 0
    return render(request,"myexpense/search.html",{'lists':lists,"total_amount":total_amount})


