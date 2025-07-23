from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login ,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trip, Expense,Category
def home(request):
    return render(request,'home.html')
def admin_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"sorry you'r not admin/staff")
                return redirect('login')
        else:
           messages.error(request,'please check password | username')
           return redirect('Admin')
    return render(request,'admin.html')
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'login successfull')
            return redirect('home')
        else:
           messages.error(request,'please check the details properly')
           return redirect('login')
    return render(request,'user.html')
def logout_view(request):
    logout(request)
    return redirect('login')
def register(request):
    if request.method =='POST':
        First_Name = request.POST['name']
        Email=request.POST['email']
        username =request.POST['username']
        password =request.POST['password']
        confirmation_password =request.POST['cnfm_password']
        select_user=request.POST['select_user']
        if select_user == 'admin':
            select_user=True
        else :
            select_user=False
        if password == confirmation_password:
            user = User.objects.filter(username=username)
            if user:
                messages.error(request,'username already exist use different')
                return redirect('register')
            else:
                user=User.objects.create_user(
                    username=username,
                    password=password,
                    email=Email,
                    first_name=First_Name,is_staff=select_user)
                user.save()
                messages.success(request,'created account successfully')
                return redirect('login')
        else:
            messages.error(request,'password should same password twice')
            return redirect('register')
    return render(request,'register.html')
def trip_list(request):
    trips = Trip.objects.all()
    return render(request, 'trip_list.html', {'trips': trips})
def add_trip(request):
    if request.method=="POST":
        name = request.POST['trip']
        start_date = request.POST['start_date']
        end_date =request.POST['end_date']
        data=Trip.objects.create(user=request.user,name=name,start_date=start_date,end_date=end_date)
    return render(request, 'add_trip.html')
def add_expense(request):
    category=Category.objects.all()
    trip=Trip.objects.filter(user=request.user,status='pending')
    if request.method=="POST":
        trip_id=request.POST['Trip']
        category_id=request.POST['category']
        Date=request.POST['date']
        price=request.POST['price']
        Description=request.POST['description']
        trip=Trip.objects.get(id=trip_id)
        category=Category.objects.get(id=category_id)
        data=Expense.objects.create(trip=trip,category=category,date=Date,amount=price,description=Description)
        data.save()
        return redirect('add_expense')
    return render(request, 'add_expense.html', {'categories': category,'trips':trip})
def add_category(request):
    categories=Category.objects.all()
    if request.method=="POST":
        category=request.POST['category']
        data=Category.objects.create(name=category)
        messages.success(request,'Saved expense Sucessfully')
        return redirect('add_category')
    return render(request,'add_category.html',{'categories':categories})
def trip_list(request):
    trips=Trip.objects.filter(user=request.user)
    return render(request,'trip_list.html',{'trips':trips})
def expense_list(request,pk):
    trip=Trip.objects.get(id=pk,user=request.user)
    expenses=Expense.objects.filter(trip=trip)
    amount=sum(item.amount for item in expenses)
    return render(request,'expenselist.html',{'expenses':expenses,'trip':trip,'amount':amount})    
def finsih_trip(request,pk):
    trip=Trip.objects.get(id=pk,user=request.user)
    if trip.status == 'pending':
        trip.status = 'Done'
        trip.save()
    return redirect('trips_list')    


