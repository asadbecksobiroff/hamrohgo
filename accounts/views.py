from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from .models import TelegramProfile, Car, Roles
from .utils import verify_telegram_init_data
import json

@csrf_exempt
def auth_telegram(request):
    """
    Endpoint to authenticate user via Telegram initData.
    Expects POST request with 'initData'.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            init_data = data.get('initData')
            tg_user = verify_telegram_init_data(init_data)
            
            if not tg_user:
                return JsonResponse({'status': 'error', 'message': 'Invalid Telegram data'}, status=403)
            
            tg_id = tg_user.get('id')
            profile = TelegramProfile.objects.filter(telegram_id=tg_id).first()
            
            if not profile:
                # Create new user
                username = tg_user.get('username') or f"user_{tg_id}"
                user = User.objects.create_user(username=username)
                profile = TelegramProfile.objects.create(
                    user=user,
                    telegram_id=tg_id,
                    first_name=tg_user.get('first_name'),
                    last_name=tg_user.get('last_name'),
                    username=tg_user.get('username'),
                    language_code=tg_user.get('language_code'),
                    photo_url=tg_user.get('photo_url')
                )
            else:
                user = profile.user
                # Update profile data if changed
                profile.first_name = tg_user.get('first_name')
                profile.last_name = tg_user.get('last_name')
                profile.username = tg_user.get('username')
                profile.language_code = tg_user.get('language_code')
                profile.photo_url = tg_user.get('photo_url')
                profile.save()

            # Login user without password
            login(request, user)

            return JsonResponse({
                'status': 'success',
                'user': {
                    'username': user.username,
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'telegram_id': profile.telegram_id
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


def auth_telegram_login(request):
    """
    Render login page of the Mini App.
    """
    return render(request, 'accounts/login.html')

@login_required
def profile_view(request):
    user = request.user
    try:
        tg_user = user.telegram_profile
    except Exception:
        tg_user = None

    data = {
        'user': user,
        'tg_user': tg_user,
    }
    return render(request, 'accounts/profile.html', data)

class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = TelegramProfile
    template_name = 'accounts/profile_edit.html'
    fields = ('first_name', 'last_name', 'phone', 'region', 'city',)
    success_url = reverse_lazy('profile')

class CarCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Car
    template_name = 'accounts/car_create.html'
    fields = ('model', 'brand', 'seats', 'number', 'color', 'photo_url', 'car_type',)
    success_url = reverse_lazy('profile')

    def test_func(self):
        user = self.request.user
        try:
            tg_user = user.telegram_profile
            tg_user_role = tg_user.role
        except Exception:
            tg_user_role = None
            
        if not (user.is_staff or tg_user_role in (Roles.DRIVER, Roles.ADMIN)):
            return False
        if Car.objects.filter(driver=user).exists():
            return False
        
        return True
    
    def form_valid(self, form):
        if self.request.POST:
            number = self.request.POST['number']
            if Car.objects.filter(number=number).exists():
                raise ValidationError(message="Number is already exist")
            form.instance.driver = self.request.user
        return super().form_valid(form)
    

class CarUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Car
    template_name = 'accounts/car_edit.html'
    fields = ('model', 'brand', 'seats', 'number', 'color', 'photo_url', 'car_type',)
    success_url = reverse_lazy('profile')

    def test_func(self):
        user = self.request.user
        try:
            tg_user = user.telegram_profile
            tg_user_role = tg_user.role
        except Exception:
            tg_user_role = None
            
        if not (user.is_staff or tg_user_role in (Roles.DRIVER, Roles.ADMIN)):
            return False
        if not Car.objects.filter(driver=user).exists():
            return False
        
        return True

    def form_valid(self, form):
        if self.request.POST:
            number = self.request.POST['number']
            if Car.objects.filter(number=number).exists():
                raise ValidationError(message="Number is already exist")
        return super().form_valid(form)
    

class CarDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Car
    template_name = 'accounts/car_delete.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        user = self.request.user
        try:
            tg_user = user.telegram_profile
            tg_user_role = tg_user.role
        except Exception:
            tg_user_role = None
            
        if not (user.is_staff or tg_user_role in (Roles.DRIVER, Roles.ADMIN)):
            return False
        if not Car.objects.filter(driver=user).exists():
            return False
        
        return True