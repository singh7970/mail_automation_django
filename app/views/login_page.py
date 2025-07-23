from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Register
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(email=email)
            if user.check_password(password):
                auth_login(request, user)  # ✅ Django login!

                messages.success(request, f"Welcome, {user.first_name}!")

                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('subscription')
            else:
                messages.error(request, "Invalid email or password.")
        except Register.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, "login.html")