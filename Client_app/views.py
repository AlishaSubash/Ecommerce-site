from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect,render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.urls import reverse
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import *


def AddProduct(request):
    c = category.objects.all()
    if request.method == 'POST':
        pname = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        pimage = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(pimage.name, pimage)
        description = request.POST.get('description')
        cat = request.POST.get('categ')
        catobj = category.objects.get(id=cat)  # <-- FIXED HERE
        product.objects.create(
            name=pname,
            price=price,
            stock=stock,
            product_image=filename,
            description=description,
            categ=catobj
        )
        return HttpResponse("Product Added Successfully")
    return render(request, 'sample.html', {'categories': c})


def register(request):
    if request.method == 'POST':
        sname = request.POST.get('name')
        slname = request.POST.get('lname')
        semail = request.POST.get('email') 
        susername = request.POST.get('username')
        spassword = request.POST.get('password')
        User.objects.create_user(first_name=sname, last_name=slname, email=semail, username=susername, password=spassword)
    return render(request, 'sign.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        psw = request.POST.get('password')
        user = authenticate(request, username=username, password=psw)
        if user:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard')
            return redirect('home')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return render(request, 'login.html', {'message': 'You have been logged out.'})


# views.py
def home_view(request):
    categories = category.objects.all()
    selected_category = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    products = product.objects.all()
    if selected_category != 'all':
        products = products.filter(categ__id=selected_category)
    if search_query:
        products = products.filter(name__icontains=search_query)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    })



def edit_products(request):
    categories = category.objects.all()
    selected_category = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '')
    products = product.objects.all()
    if selected_category != 'all':
        products = products.filter(categ__id=selected_category)
    if search_query:
        products = products.filter(name__icontains=search_query)
    return render(request, 'edit_products.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    })


def delete_product(request, product_id):
    prod = get_object_or_404(product, id=product_id)
    if request.method == 'POST':
        prod.delete()
        return redirect('edit_products')
    return redirect('edit_product', product_id=product_id)


def edit_product(request, product_id):
    prod = product.objects.get(id=product_id)
    categories = category.objects.all()
    if request.method == 'POST':
        prod.name = request.POST.get('name')
        prod.price = request.POST.get('price')
        prod.stock = request.POST.get('stock')
        prod.description = request.POST.get('description')
        cat_id = request.POST.get('categ')
        prod.categ = category.objects.get(id=cat_id)
        if 'image' in request.FILES:
            prod.product_image = request.FILES['image']
        prod.save()
        return redirect('product_detail', product_id=prod.id)
    return render(request, 'edit_product.html', {'product': prod, 'categories': categories})

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = 0
    for item in items:
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        qty = int(request.POST.get('qty', 1))
        if qty > 0:
            item.quantity = qty
            item.save()
        else:
            item.delete()
    return redirect('cart')


def product_detail(request, product_id):
    prod = get_object_or_404(product, id=product_id)
    return render(request, 'product_detail.html', {'product': prod})


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        login_url = reverse('login')
        add_to_cart_url = reverse('add_to_cart', args=[product_id])
        return redirect(f'{login_url}?next={add_to_cart_url}')
    prod = get_object_or_404(product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=prod)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required
def proceed_to_payment(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    unavailable = []
    total = 0
    for item in items:
        if item.quantity > item.product.stock:
            unavailable.append({
                'name': item.product.name,
                'requested': item.quantity,
                'available': item.product.stock
            })
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal
    if unavailable:
        return render(request, 'cart_unavailable.html', {'unavailable': unavailable})
    return render(request, 'payment.html', {'items': items, 'total': total})


@login_required
def place_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    if not items:
        return redirect('cart')
    total = sum(item.product.price * item.quantity for item in items)
    # Create the order
    order = admin_order.objects.create(user=request.user, total=total)
    # Create order items
    for item in items:
        admin_order_item.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        # Optionally, update product stock
        item.product.stock -= item.quantity
        item.product.save()
    # Clear the cart
    items.delete()
    return render(request, 'order_success.html', {'order': order})


def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_orders(request):
    search_id = request.GET.get('order_id', '')
    orders = admin_order.objects.prefetch_related('items__product', 'user').all().order_by('-created_at')
    if search_id:
        orders = orders.filter(id=search_id)
    return render(request, 'admin_orders.html', {'orders': orders, 'search_id': search_id})


def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(admin_order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in dict(admin_order.STATUS_CHOICES):
            # If changing from not-cancelled to cancelled, restore stock
            if order.status != 'Cancelled' and new_status == 'Cancelled':
                for item in order.items.all():
                    item.product.stock += item.quantity
                    item.product.save()
            order.status = new_status
            order.save()
    return redirect('admin_orders')

#rest api views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    User_data=User.objects.all()
    serializer= UserSerializer(User_data, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def post_user_details(request):
    if request.method == 'POST':
        sname = request.POST.get('name')
        slname = request.POST.get('lname')
        semail = request.POST.get('email') 
        susername = request.POST.get('username')
        spassword = request.POST.get('password')
        User.objects.create_user(first_name=sname, last_name=slname, email=semail, username=susername, password=spassword)
        return Response("Success")
    # Always return a Response for GET or other methods
    return Response("Send a POST request to create a user.")

@api_view(['PUT','GET'])
def update_user_details(request, user_id):
    user=User.objects.filter(id=user_id)
    if request.method=='PUT':
        sname = request.POST.get('name')
        slname = request.POST.get('lname')
        semail = request.POST.get('email') 
        susername = request.POST.get('username')
        spassword = request.POST.get('password')
        user.update(first_name=sname, last_name=slname, email=semail, username=susername, password=spassword)
        return Response("User details updated successfully")
    
    return Response("provide a valid data")
    
@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    user.delete()
    return Response({"message": "User deleted"})


@login_required
def user_orders(request):
    orders = admin_order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'user_orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(admin_order, id=order_id, user=request.user)
    if request.method == 'POST' and order.status not in ['Cancelled', 'Completed']:
        order.status = 'Cancelled'
        order.save()
        # Optionally restore stock here
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False})
    return redirect('user_orders')

def admin_reports(request):
    total_products = product.objects.count()
    total_in_stock = product.objects.aggregate(total=Sum('stock'))['total'] or 0
    total_orders = admin_order.objects.count()
    total_sales = admin_order.objects.filter(status='Completed').aggregate(total=Sum('total'))['total'] or 0
    sales_by_month = (
        admin_order.objects.filter(status='Completed')
        .extra({'month': "strftime('%%Y-%%m', created_at)"})
        .values('month')
        .annotate(total=Sum('total'))
        .order_by('month')
    )
    top_products = (
        admin_order_item.objects.values('product__name')
        .annotate(sold=Sum('quantity'))
        .order_by('-sold')[:5]
    )
    context = {
        'total_products': total_products,
        'total_in_stock': total_in_stock,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'sales_by_month': list(sales_by_month),
        'top_products': list(top_products),
    }
    return render(request, 'admin_reports.html', context)