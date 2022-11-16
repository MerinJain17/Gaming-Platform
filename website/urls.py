from django.contrib import admin
from django.urls import path
from website import views

urlpatterns = [
    path('', views.index,name='website'),
    path('play', views.play,name='play'),
    path('about', views.about,name='about'),
    path('contact', views.contact,name='contact'),
    path('account', views.account,name='account'),
    path('login', views.login,name='login'),
    path('random', views.random,name='random'),
    path('game1', views.game1,name='game1'),
    path('game2', views.game2,name='game2'),
    path('game3', views.game3,name='game3'),
    path('game4', views.game4,name='game4'),
    path('game5', views.game5,name='game5'),
    path('game6', views.game6,name='game6'),
     path('activation_fail', views.activation_fail,name='activation_fail'),
    
    path('activate/<uidb64>/<token>',views.activate,name="activate")
]