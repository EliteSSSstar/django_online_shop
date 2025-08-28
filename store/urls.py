from django.urls import path
from . import views
from .views import home, product_list, login_view, logout_view, user_list, promote_to_manager, create_staff, staff_dashboard, manager_dashboard

urlpatterns = [
    path('', home, name='home'),  # Root URL now goes to home.html
    path('home/', home, name='home_alt'),  # Optional secondary link
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('products/', product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('manage-users/', manager_dashboard, name='manage_users'),  # <-- updated here to user_list
    path('user-list/', user_list, name='user_list'),
    path('create_staff/', create_staff, name='create_staff'),
    path('promote_staff/<int:user_id>/', promote_to_manager, name='promote_staff'),
    path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),

]
