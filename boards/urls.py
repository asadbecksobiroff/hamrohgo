from django.urls import path
from .views import index, BoardsListView, BoardCreateView, BoardDetailView, BoardUpdateView, BoardDeleteView

urlpatterns = [
    path('', index, name='home'),
    path('board/', BoardsListView.as_view(), name='board'),
    path('board/detail/<int:pk>/', BoardDetailView.as_view(), name='board_detail'),
    path('board/create/', BoardCreateView.as_view(), name='board_create'),
    path('board/update/<int:pk>/', BoardUpdateView.as_view(), name='board_update'),
    path('board/delete/<int:pk>/', BoardDeleteView.as_view(), name='board_delete'),
]