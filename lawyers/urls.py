from django.urls import path
from . import views

urlpatterns = [
    path('lawyer-login/', views.lawyer_login, name='lawyer_login'),
    path('signup/', views.lawyer_signup, name='lawyer_signup'),
    path('lawyer-dahboard/',views.lawyer_dashboard,name='lawyer_dashboard'),
    path('lawyer-profile/',views.lawyer_profile,name='lawyer_profile'),
    path('editprofile/' ,views.edit_lawyer_profile,name='edit_lawyer_profile'),
    path ('change-password/',views.lawyer_change_password,name='lawyer_change_password'),
    path('logout/',views.lawyer_logout,name='lawyer_logout'),

]