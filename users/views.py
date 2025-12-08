# # Create your views here.
# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from django.contrib import messages
# from .models import User
# from lawyer.models import LawyerProfile
# from django.contrib.auth.hashers import make_password


# def lawyer_signup(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         phone = request.POST.get("phone")
#         password = request.POST.get("password")

#         # Check existing user
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists")
#             return redirect("lawyer_signup")

#         # Create User
#         user = User.objects.create(
#             username=email,
#             email=email,
#             first_name=name,
#             phone=phone,
#             role='lawyer',
#             password=make_password(password),
#         )

#         # Create empty lawyer profile
#         LawyerProfile.objects.create(
#             user=user,
#             verification_status='pending'
#         )

#         messages.success(request, "Signup successful. Admin will verify your account")
#         login(request, user)
#         return redirect("lawyer_dashboard")

#     return render(request, "users/lawyer_signup.html")
