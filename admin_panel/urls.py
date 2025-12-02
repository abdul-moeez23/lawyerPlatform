from django.urls import include,path
from .import views

urlpatterns = [
    path('login/',views.admin_login,name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('pending-lawyers/', views.pending_lawyer_requests, name='pending_lawyer_requests'),
    path('approve-lawyer/<int:id>/', views.approve_lawyer, name='approve_lawyer'),

    # view approved lawyers
    path('approvedlawyer',views.approved_lawyers,name='approved_lawyers')
]

