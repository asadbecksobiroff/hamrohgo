from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.models import Car, Roles
from .models import Board

class TestDriverMixin(LoginRequiredMixin, UserPassesTestMixin):
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