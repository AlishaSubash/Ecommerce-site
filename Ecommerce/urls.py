"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Client_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product-add',views.AddProduct,name='add'),
    path('signup',views.register,name='signup'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('home', views.home_view, name='home'),
    path('', views.login_view, name='login'),  # Default login view
    path('edit-products/', views.edit_products, name='edit_products'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cart/', views.cart_view, name='cart'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('proceed-to-payment/', views.proceed_to_payment, name='proceed_to_payment'),
    path('place-order/', views.place_order, name='place_order'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-orders/update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('orders/', views.user_orders, name='user_orders'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('admin-reports/', views.admin_reports, name='admin_reports'),

    #rest api urls
    path('get_user_details/', views.get_user_details, name='get_user_details'),
    path('post_user_details', views.post_user_details, name='post_user_details'),
    path('update_user_details/<int:user_id>/', views.update_user_details, name='update_user_details'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)