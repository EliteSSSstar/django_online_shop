from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib import messages
# llalala
def home(request):
    return render(request, 'store/home.html')

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_staff(user):
    return user.is_staff

@login_required
def product_list(request):
    if request.user.is_staff or is_manager(request.user):
        return render(request, 'store/manager_dashboard.html')
    else:
        products = Product.objects.all()
        return render(request, 'store/products_list.html', {'products': products})

def cart(request):
    return render(request, 'store/cart.html')  # Placeholder

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if is_manager(user):
                return redirect('manage_users')
            elif user.is_staff:
                return redirect('products_list')
            else:
                return redirect('products_list')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'store/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_manager)
def user_list(request):
    users = User.objects.all()
    return render(request, 'store/user_list.html', {'users': users})

@login_required
@user_passes_test(is_manager)
def promote_staff(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_staff = True
    user.save()
    messages.success(request, f"{user.username} has been promoted to staff.")
    return redirect('manage_users')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'store/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'store/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'store/register.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')

    return render(request, 'store/register.html')


# Only allow managers or superusers to view
@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Manager').exists())
def user_list(request):
    users = User.objects.all()
    return render(request, 'store/user_list.html', {'users': users})