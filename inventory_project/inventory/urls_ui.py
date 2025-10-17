from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.item_list_view, name='item_list_ui'),
    path('items/<int:pk>/', views.item_detail_view, name='item_detail_ui'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
