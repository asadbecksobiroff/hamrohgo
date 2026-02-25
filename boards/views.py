from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User

def index(request):
    """
    Render main page of the Mini App.
    """
    if request.user.is_authenticated:
        user = request.user
        try:
            tg_user = user.telegram_profile
        except Exception:
            tg_user = None
            
        data = {
            'user': user,
            'telegram_profile': tg_user
        }
        return render(request, 'boards/home.html', data)
    else:
        return redirect('auth_telegram_login')
