from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', ProfileView.as_view(), name='profile_view'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='profile_delete'),

    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('cart/cart/', CartListView.as_view(), name='cart_detail'),
    path('cart/cart/add/', CreateToCartView.as_view(), name='cart_add'),
    path('cart/cart/delete/<int:pk>/', CartDeleteView.as_view(), name='cart_delete'),
    path('cart/order/create/', OrderCreateView.as_view(), name='order_create'),
    path('cart/orders/', OrderListView.as_view(), name='order_list'),

    path('logout/', logout, name='logout'),
]