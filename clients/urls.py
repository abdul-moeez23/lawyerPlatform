from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    # path('signin/', views.client_signin, name='client_signin'),
    # path('signup/', views.client_signup, name='client_signup'),
    # path('logout/', views.client_logout, name='client_logout'),
    path('signin/',views.signin,name='signin'),
    path('lawyers/search/', views.search_lawyers, name='search_lawyers'),  
    
    # Dashboard URLs
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
    path('my-cases/', views.my_cases, name='my_cases'),
    path('case/<int:pk>/', views.case_detail, name='case_detail'),
    path('profile/', views.client_profile, name='client_profile'),
]
