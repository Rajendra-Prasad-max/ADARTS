import pyotp
import qrcode
import io
import base64
import binascii
from shop.models import Order
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .forms import UserEditForm, UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth import get_user_model


User = get_user_model()

@login_required
def enable_totp(request):
    user = request.user
    if request.method == 'POST':
        if 'generate_qr' in request.POST:
            # Generate a new TOTP secret and device for the user
            totp_secret = pyotp.random_base32()
            totp = pyotp.TOTP(totp_secret)
            provisioning_uri = totp.provisioning_uri(name=user.email, issuer_name='YourAppName')

            # Save the TOTP secret in the user's session temporarily
            request.session['totp_secret'] = totp_secret

            # Generate QR code image
            qr = qrcode.make(provisioning_uri)
            buf = io.BytesIO()
            qr.save(buf, format='PNG')
            qr_code = base64.b64encode(buf.getvalue()).decode('utf-8')

            return render(request, 'enable_totp.html', {'qr_code': qr_code})

        elif 'enable_totp' in request.POST:
            totp_secret = request.session.get('totp_secret')
            if totp_secret:
                # Convert the base32 secret to hexadecimal
                hex_key = binascii.hexlify(base64.b32decode(totp_secret)).decode()

                # Store the TOTPDevice in the database
                TOTPDevice.objects.create(user=user, confirmed=True, key=hex_key)

                # Clear the session variable
                del request.session['totp_secret']

                # Redirect to verify_totp view
                request.session['pre_2fa_user_id'] = user.id
                return redirect('verify_totp')

            else:
                messages.error(request, 'Failed to enable TOTP. Please try again.')

    return render(request, 'enable_totp.html')


def verify_totp(request):
    pre_2fa_user_id = request.session.get('pre_2fa_user_id')
    if not pre_2fa_user_id:
        return redirect('login')

    user = User.objects.get(id=pre_2fa_user_id)

    if request.method == 'POST':
        token = request.POST['token']
        try:
            totp_device = TOTPDevice.objects.get(user=user)
            if totp_device.verify_token(token):
                login(request, user)
                del request.session['pre_2fa_user_id']
                messages.success(request, 'TOTP verification successful!')
                return redirect('home')  # Replace 'home' with the URL name of your homepage view
            else:
                messages.error(request, 'Invalid TOTP token.')
        except TOTPDevice.DoesNotExist:
            messages.error(request, 'TOTP device not enabled.')

    return render(request, 'verify_totp.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        otp = request.POST.get('otp')  # Capture OTP from the form
        if form.is_valid():
            user = request.user
            device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
            if device and device.verify_token(otp):  # Verify the OTP
                form.save()
                update_session_auth_hash(request, form.user)  # Prevents the user from being logged out
                messages.success(request, 'Your password was successfully updated!')
                return redirect('change_password')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_pwd.html', {'form': form })


@login_required
def user_update(request, id=None):
    instance = get_object_or_404(User, id=id)
    form = UserEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/user/details/{0}".format(instance.id))

    context = {
              'instance': instance,
              'form': form,
    }
    return render(request, "user/edit.html", context)


@login_required
def user_detail(request, id=None):
    instance = get_object_or_404(User, id=id)
    context = {
            'instance': instance,
    }
    return render(request, "user/details.html", context)


@login_required
def my_orders(request):
    orders = Order.objects.filter(user_id=request.user.id)
    context = {
            'orders': orders,
    }
    return render(request, "user/myorders.html", context)


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('enable_totp')  # Redirect to enable TOTP
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                totp_device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
                if totp_device:
                    request.session['pre_2fa_user_id'] = user.id
                    return redirect('verify_totp')
                else:
                    login(request, user)
                    return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})