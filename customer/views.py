

from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel
import json
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customers/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customers/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # Get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entrees = MenuItem.objects.filter(category__name__contains='Entree')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # Pass into context
        context = {
            'appetizers': appetizers,
            'entres': entrees,
            'desserts': desserts,
            'drinks': drinks,
        }

        # Render the template
        return render(request, 'customers/order.html', context)


    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        # accounts = request.POST.get('accounts')

        order_items = {
        'items': []
    }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(price=price,
                                          name=name,
                                          email=email,
                                          street=street,
                                          city=city,
                                          state=state,
                                          zip=zip)
        order.items.add(*item_ids)

        # After all this now send mail to user
        body = 'Thank You for your Order! Your food is being made and will be delivered soon!\n' + \
       f'Your Total: {price}\n' + \
       'Have a good time'

        send_mail('Thank You for your Order!', body, 'example@example.com', [email], fail_silently=False)
   

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,

        }
        return render(request, 'customers/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()
        return redirect('payment-confirmation')   

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customers/order_pay_confirmation.html')
    
class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()
        context = {
            'menu_items': menu_items
        }
        return render(request, 'customers/menu.html', context)

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )
        context = {
            'menu_items': menu_items
        }
        return render(request, 'customers/menu.html', context)
    
@login_required(login_url='login')
def HomePage(request):
    return render(request, 'customers/index.html')
    
def SignUp(request):
        if request.method == 'POST':
            uname = request.POST.get('username')
            email = request.POST.get('email')
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')

            if pass1 != pass2:
                return HttpResponse("Username or Password is Incorrect!!")
            else:
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                return redirect('login')
    
        return render(request, 'customers/signup.html')

def LogIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password = pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is Incorrect!!!")

    return render(request, 'customers/login.html')

def LogOutPage(request):
    logout(request)
    return redirect('login')