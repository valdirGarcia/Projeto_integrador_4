from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('filme/<int:pk>/', views.detalhes_filme, name='detalhes_filme'),  # URL para detalhes do filme
]
