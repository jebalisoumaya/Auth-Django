from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"user": request.user.username})


@login_required
@ensure_csrf_cookie
def current_user_view(request):
    """Vue qui affiche le nom d'utilisateur connecté avec gestion CSRF"""
    if request.method == 'GET':
        if request.headers.get('Accept') == 'application/json':
            # Réponse JSON pour les requêtes AJAX
            return JsonResponse({
                'username': request.user.username,
                'email': request.user.email,
                'is_authenticated': request.user.is_authenticated,
                'csrf_token': request.META.get('CSRF_COOKIE')
            })
        else:
            # Réponse HTML pour le navigateur
            context = {
                'user': request.user,
                'username': request.user.username,
                'email': request.user.email
            }
            return render(request, 'api/current_user.html', context)


@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vue de connexion avec gestion CSRF"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'username': user.username})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
    
    # GET request - afficher le formulaire de connexion
    return render(request, 'api/login.html')


@login_required
def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logged out successfully'})
