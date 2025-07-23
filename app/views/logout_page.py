from django.contrib.auth import logout

from django.shortcuts import render, redirect

def logout_view(request):
    logout(request)
    return redirect('login_page')  # 👈 change to your login page URL name