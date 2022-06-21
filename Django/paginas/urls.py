from django.urls import path
from .views import IndexView

urlpatterns = [
  # path(endereço/, ClasseView.as_view(), nome='nome-da-url') 
    path('', IndexView.as_view(), name='inicio')    
]
