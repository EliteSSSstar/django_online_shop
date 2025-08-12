from django.urls import path
from . import views
from .views import home, product_list, login_view, logout_view, user_list, promote_staff

urlpatterns = [
    path('', home, name='home'),  # Root URL now goes to home.html
    path('home/', home, name='home_alt'),  # Optional secondary link
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('products/', product_list, name='product_list'),
    path('manage-users/', user_list, name='manage_users'),  # <-- updated here to user_list
    path('promote_staff/<int:user_id>/', promote_staff, name='promote_staff'),
]
