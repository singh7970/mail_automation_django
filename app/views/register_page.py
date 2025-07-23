from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from app.models import Register




def register_page(request):
    if request.method == 'POST':
        
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check if email already exists
        if Register.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register_page")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register_page")

        # ✅ Step 1: Create user without password
        user = Register(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save()  # Saves and assigns primary key

        # ✅ Step 2: Set hashed password
       

        messages.success(request, "Registration successful. Please log in.")
        return redirect("login_page")

    return render(request, "register.html")
