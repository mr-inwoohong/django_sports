from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name = 'home'),
    path('headlines/<str:searchterm>/', views.get_headlines, name='headlines'),
    path('psa/<int:cert_number>/', views.psa, name='psa'),
    path('current/<str:searchterm>/', views.get_current, name='current'),
    path('sold/<str:searchterm>/', views.get_data, name='get_data'),
    path('nba/<str:player_name>/<int:season>/', views.nba_stats, name='nba_stats'),
    path('baseball/<str:player_name>/', views.player_batting_stats, name='player_batting_stats'),
]
