from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from .models import Board
from .custom_mixins import TestDriverMixin

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
    
class BoardsListView(ListView):
    model = Board
    template_name = 'boards/board.html'
    context_object_name = 'boards'

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        if Board.objects.filter(driver=self.request.user).exists():
            data['has_board'] = True
            data['board_id'] = Board.objects.get(driver=self.request.user).id
        else:
            data['has_board'] = False

        try:
            data['user_role'] = self.request.user.telegram_profile.role
        except Exception:
            data['user_role'] = None

        return data

class BoardCreateView(TestDriverMixin, CreateView):
    model = Board
    template_name = 'boards/board_create.html'
    fields = ('seats', 'from_region', 'from_city', 'to_region', 'to_city', 'price', 'comment',)
    def get_success_url(self):
        return reverse('board_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.request.POST:
            form.instance.driver = self.request.user
        return super().form_valid(form)

    def test_func(self):
        permssion = super().test_func()
        if Board.objects.filter(driver=self.request.user).exists():
            return False
        return permssion
    
class BoardDetailView(TestDriverMixin, DetailView):
    model = Board
    template_name = 'boards/board_detail.html'
    context_object_name = 'board'


class BoardUpdateView(TestDriverMixin, UpdateView):
    model = Board
    template_name = 'boards/board_update.html'
    fields = ('seats', 'from_region', 'from_city', 'to_region', 'to_city', 'price', 'comment',)
    def get_success_url(self):
        return reverse('board_detail', kwargs={'pk': self.object.pk})
    
class BoardDeleteView(TestDriverMixin, DeleteView):
    model = Board
    template_name = 'boards/board_delete.html'
    success_url = reverse_lazy('board')