from django.http import HttpResponse
from django.shortcuts import redirect, render,  get_object_or_404
from cart.models import UserCart
import razorpay
from django.conf import settings
from shop.models import Product, Order
from django.views.decorators.csrf import csrf_exempt
from .forms import CheckoutForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cart.models import UserCart

# Create your views here.
def cart_page(request):
    if not request.user.is_authenticated:
        return redirect('/')

    cart_items = UserCart.objects.filter(user_id=request.user.id, in_cart=True)
    total = sum(item.product.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'cart/cart.html', context)

def order_placed(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.GET.get('message'):
        return redirect('/')
    return render(request, 'cart/thankyou.html', {'msg': request.GET['message']})

def add_product_to_cart(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.method == 'GET':
        product_id = request.GET.get('id')
        quantity = int(request.GET.get('quantity', 1))  # Default to 1 if not provided
        product = get_object_or_404(Product, pk=product_id)
        cart_item, created = UserCart.objects.get_or_create(user=request.user, product=product, in_cart=True)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()
        return redirect("/cart")
    return HttpResponse('Only GET method allowed')
def remove_product_from_cart(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        cart_item_id = request.GET.get('id')
        cart_item = get_object_or_404(UserCart, id=cart_item_id)
        cart_item.delete()
        return redirect("/cart")
    return HttpResponse('Only GET method allowed')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    cart_items = UserCart.objects.filter(user_id=request.user.id, in_cart=True)
    total = sum(item.product.price * item.quantity for item in cart_items)
    orderdetails = ', '.join(f"{item.product.name} x {item.quantity}" for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            delivery_address = f"{form.cleaned_data['name']}, {form.cleaned_data['address1']}, " \
                               f"{form.cleaned_data.get('address2', '')}, {form.cleaned_data['city']}, " \
                               f"{form.cleaned_data['state']}, {form.cleaned_data['pincode']} - {form.cleaned_data['mobile']}"
            order = Order.objects.create(
                user_id=request.user.id,
                amount=total,
                delivery_address=delivery_address,
                details=orderdetails
            )
            # Razorpay order creation
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create({
                "amount": total * 100,  # amount in paisa
                "currency": "INR",
                "payment_capture": "1"
            })
            order.razorpay_order_id = razorpay_order['id']
            order.save()

            context = {
                'cart_items': cart_items,
                'total': total,
                'order_id': razorpay_order['id'],
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'user_email': request.user.email,
                'user_name': request.user.username,
                'delivery_address': delivery_address
            }
            return render(request, 'cart/payment.html', context)
        return render(request, 'cart/checkout.html', {'form': form, 'cart_items': cart_items, 'total': total})

    form = CheckoutForm()
    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form
    }
    return render(request, 'cart/checkout.html', context)


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('order_id', '')
        try:
            order = Order.objects.get(razorpay_order_id=order_id)
            order.payment_id = payment_id
            order.status = 'Paid'
            order.save()
            UserCart.objects.filter(user_id=order.user.id, in_cart=True).update(in_cart=False)
            return redirect('/cart/order-placed?message=Your order has been placed successfully. Thank you!')
        except Order.DoesNotExist:
            return HttpResponse('Order does not exist', status=400)
    return HttpResponse('Invalid request', status=400)


@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('id')
        quantity = int(request.POST.get('quantity'))
        cart_item = get_object_or_404(UserCart, id=cart_item_id)
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})