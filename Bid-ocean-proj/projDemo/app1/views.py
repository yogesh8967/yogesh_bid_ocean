from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import json
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, admin_only

@unauthenticated_user
def register(request):
	
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user_main = form.save()
				user = form.cleaned_data.get('username')
				user_mail = form.cleaned_data.get('email')
				group = Group.objects.get(name='customers')
				user_main.groups.add(group)
				messages.success(request, 'Account was created for ' + user)
				Profile_instance = Profile.objects.create(User_ID = user, E_Mail = user_mail)
				return redirect('login')
			

		context = {'form':form}
		return render(request, 'app1/register.html', context)

@unauthenticated_user
def login_p(request):
	
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				person = Profile.objects.get(User_ID = username)
				print("PERSON IS HERE ",person.Address)
				if request.user.groups.exists():
					group = request.user.groups.all()[0].name
					if group == 'manager':
						return redirect('manager')
				elif person.Address == None or person.Ph_no == None:
					return redirect('add_details' + '/' + person.User_ID + '/')
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')
				return redirect('login')

		context = {}
		return render(request, 'app1/login.html', context)

def logouter(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def details_adder(request, usr):
	person = Profile.objects.get(User_ID = usr)
	form = ProfileForm(instance=person)
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance = person)
		if form.is_valid():
			form.save()
			return redirect('home')
	context = {'person': form}
	return render(request, 'app1/add_details.html', context)



@login_required(login_url='login')
@admin_only
def manager_control(request):
	return render(request, 'app1/manager.html')

@login_required(login_url='login')
@admin_only
def Dish_Adder(request):
	form = DishForm()
	if request.method == 'POST':
		form = DishForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('manager')
	context = {'dishF': form}
	return render(request, 'app1/Add_Dish.html', context)

@login_required(login_url='login')
@admin_only
def Dishes(request):
	dishes = Dish.objects.all()
	All_Dishes = {'dishes': dishes}
	return render(request, 'app1/Dishes.html', All_Dishes)

@login_required(login_url='login')
@admin_only
def Orders(request):
	order_list = {'orders': [] }
	orders = Order.objects.all().order_by('Date')
	orders = orders.reverse()
	for order in orders:
		ord_obj = {}
		ord_obj['order'] = order
		order_items = Intermediate.objects.filter(Order_ID = order)
		ord_obj['items'] = order_items
		order_list['orders'].append(ord_obj)
	return render(request, 'app1/Orders.html', order_list)

@login_required(login_url='login')
@admin_only
def Update_Dish(request):
	I_Dishes = Dish.objects.filter(Dish_Type = 'Indian')
	C_Dishes = Dish.objects.filter(Dish_Type = 'Chinesse')
	W_Dishes = Dish.objects.filter(Dish_Type = 'Western')
	B_Dishes = Dish.objects.filter(Dish_Type = 'Beverages')
	Dish_Cat = [{'name': 'Indian', 'content': I_Dishes}, {'name': 'Chinese', 'content': C_Dishes}, {'name': 'Western', 'content': W_Dishes}, {'name': 'Beverages', 'content': B_Dishes}]
	All_Dishes = {'Dishes': Dish_Cat}
	return render(request, 'app1/update_dish.html', All_Dishes)

@login_required(login_url='login')
@admin_only
def Updater(request, Dish_N):
	dish = Dish.objects.get(Dish_Name = Dish_N)
	form = DishForm(instance=dish)
	if request.method == 'POST':
		form = DishForm(request.POST, request.FILES,instance = dish)
		if form.is_valid():
			form.save()
			return redirect('Dishes')
	context = {'dish': form}
	return render(request, 'app1/Updater.html', context)

@login_required(login_url='login')
@admin_only
def Deleter(request, Dish_N):
	dish = Dish.objects.get(Dish_Name = Dish_N)
	if request.method == 'POST':
		dish.delete()
		return redirect('Dishes')

	All_Dishes = {'Dish': dish}
	return render(request, 'app1/Deleter.html', All_Dishes)

@login_required(login_url='login')
def home(request):
	trending = Dish.objects.all().order_by('-Total_Sold')[:4]
	new_arrival = Dish.objects.all().order_by('-Date')[:4]
	context = {'trending': trending, 'new_arrival': new_arrival}
	return render(request, 'app1/home.html', context)

@login_required(login_url='login')
def products(request):
    return render(request, 'app1/products.html')

@login_required(login_url='login')
def customer(request):
    return render(request, 'app1/customer.html')

@login_required(login_url='login')
def Menu(request, Category):
	Dish_C = Dish.objects.filter(Dish_Type = Category)
	category = {'Category': Dish_C, 'Category_name': Category}
	return render(request, 'app1/Menu.html',category)

@login_required(login_url='login')
def Menu_cart(request, Category, usr, menu_cart):
	Dish_C = Dish.objects.get(Dish_Name = usr)
	person = Profile.objects.get(User_ID = request.user.username)
	if request.method == 'POST':
		if Cart.objects.filter(Dish_id = Dish_C, User_ID = person):
			obj = Cart.objects.get(Dish_id = Dish_C, User_ID = person)
			obj.Quantity += 1
			obj.save()
		else:
			Cart.objects.create(User_ID=person, Dish_id = Dish_C, Quantity = 1)
		return HttpResponseRedirect('/cart/' + request.user.username + '/')
	category = {'Category': Dish_C}
	return render(request, 'app1/Menu.html',category)

@login_required(login_url='login')
def home_cart(request, dishname):
	Dish_C = Dish.objects.get(Dish_Name = dishname)
	person = Profile.objects.get(User_ID = request.user.username)
	if request.method == 'POST':
		if Cart.objects.filter(Dish_id = Dish_C, User_ID = person):
			obj = Cart.objects.get(Dish_id = Dish_C, User_ID = person)
			obj.Quantity += 1
			obj.save()
		else:
			Cart.objects.create(User_ID=person, Dish_id = Dish_C, Quantity = 1)
		return redirect('home')
	category = {'Category': Dish_C}
	return render(request, 'app1/Menu.html',category)

@login_required(login_url='login')
def profile_page(request, usr):
    person = Profile.objects.get(User_ID = usr)
    context = {'person':person}
    return render(request, 'app1/profile_page.html', context)

@login_required(login_url='login')
def contact_Updater(request, usr):
	print(usr)
	person = Profile.objects.get(User_ID = usr)
	print(person)
	form = ContactForm(instance = person)
	if request.method == 'POST':
		form = ContactForm(request.POST, instance = person)
		if form.is_valid():
			form.save()
			next = request.POST.get('next', '/')
			return redirect('home')
	context = {'person': form}
	return render(request, 'app1/contact_updater.html', context)

@login_required(login_url='login')
def cart(request, usr):
	person_c = Profile.objects.get(User_ID = usr)
	person = Cart.objects.filter(User_ID = person_c)
	if request.method == 'POST':
		total_cost = 0
		for i in person:
			dish = i.Dish_id
			qty = i.Quantity
			dish_obj = Dish.objects.get(Dish_Name = dish)
			total_cost = total_cost + (dish_obj.Price * qty)
		obj = Order.objects.create(User_ID = person_c, Payment_Status = 'Pending', Order_Type = 'Delivery', Destination = person_c.Address, Total_Amount = total_cost)
		obj.save()
		for i in person:
			dish = i.Dish_id
			qty = i.Quantity
			int_obj = Intermediate.objects.create(Order_ID = obj, Dish_id = dish, Quantity = qty)
			int_obj.save()
		Cart.objects.filter(User_ID = person_c).delete()
		return redirect('home')
	context = {'items': person, 'person': person_c}
	return render(request, 'app1/cart.html', context)


def myajaxtestview(request,cart,usr):
	person_obj = Profile.objects.get(User_ID = usr)
	
	print(request.body)
	data = request.POST.get('text', None) 
	data2 = request.POST.get('test', None) 
	print(data)
	print(data2)
	dish = data.split("_")
	dish_id = dish[0]
	operation = dish[1]
	current_qty = data2
	dish_obj = Dish.objects.get(id = dish_id)
	person = Profile.objects.get(User_ID = request.user.username)
	cart_obj = Cart.objects.get(Dish_id = dish_obj, User_ID = person)
	if operation == 'plus':
		cart_obj.Quantity += 1
		cart_obj.save()
	if operation == 'minus':
		cart_obj.Quantity -= 1
		if cart_obj.Quantity == 0:
			cart_obj.delete()
		else:
			cart_obj.save()
	return JsonResponse({"status": "done"})

def myajaxtestview2(request,ord):
	data = request.POST.get('text', None) 
	data2 = request.POST.get('test', None) 
	print(data)
	print(data2)
	ord_obj = Order.objects.get(id = data)
	if data2 == "Pending":
		ord_obj.Payment_Status = "Recieved"
	elif data2 == "Recieved":
		ord_obj.Payment_Status = "Pending"
	ord_obj.save()
	return JsonResponse({"status": "done"})