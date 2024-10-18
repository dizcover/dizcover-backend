from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
from django.shortcuts import render

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# Mejora: Redirigir a la página de inicio