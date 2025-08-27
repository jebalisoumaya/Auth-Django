# api/urls.py
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # API REST avec DRF
    path('whoami/', views.WhoAmIView.as_view(), name='whoami'),
    
    # Vues avec authentification par session
    path('current-user/', views.current_user_view, name='current_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
