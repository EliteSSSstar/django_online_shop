from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

from django.contrib import messages

def home(request):
    return render(request, 'store/home.html')

def is_manager(user):
    return user.is_superuser or user.groups.filter(name='managers').exists()

def is_staff(user):
    return user.is_staff

# Create staff
@login_required
@user_passes_test(is_manager)
def create_staff(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()
            # Add to employees group
            group, created = Group.objects.get_or_create(name='employees')
            user.groups.add(group)
            messages.success(request, 'Staff account created.')
        return redirect('manage_users')
    return render(request, 'store/create_staff.html')

@login_required
def product_list(request):
    if request.user.is_staff or is_manager(request.user):
        return render(request, 'store/manager_dashboard.html')
    else:
        products = Product.objects.all()
        return render(request, 'store/products_list.html', {'products': products})

def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = [
        {'product': product, 'quantity': cart[str(product.id)]}
        for product in products
    ]
    return render(request, 'store/cart.html', {'cart_items': cart_items})  # Placeholder

def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
    return redirect('cart')


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
                return redirect('staff_dashboard')
            else:
                return redirect('products_list')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'store/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def staff_dashboard(request):
    return render(request, 'store/staff_dashboard.html')


@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    users = User.objects.all()
    return render(request, 'store/manager_dashboard.html', {'users': users})


@login_required
@user_passes_test(is_manager)
def promote_to_manager(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    manager_group, _ = Group.objects.get_or_create(name='managers')
    user.groups.add(manager_group)
    user.save()
    messages.success(request, f"{user.username} promoted to Manager.")
    return redirect('manage_users')

@login_required
@user_passes_test(is_manager)
def remove_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, "User removed.")
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
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='managers').exists())
def user_list(request):
    users = User.objects.all()
    return render(request, 'store/user_list.html', {'users': users})

@login_required
@user_passes_test(is_manager)
def view_purchases(request, user_id):
    purchases = Purchase.objects.filter(user_id=user_id)
    return render(request, 'store/purchase_list.html', {'purchases': purchases})