from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    # path('signin/', views.client_signin, name='client_signin'),
    # path('signup/', views.client_signup, name='client_signup'),
    # path('logout/', views.client_logout, name='client_logout'),
    path('signin/',views.signin,name='signin'),
    path('lawyers/search/', views.search_lawyers, name='search_lawyers'),
    
]
