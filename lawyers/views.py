from django.shortcuts import render, redirect
from django.contrib import messages
# from .models import Lawyer  # assume lawyer model bana liya
from django.contrib.auth.hashers import make_password,check_password
from.models import *


def lawyer_login(request):

    if request.method == 'POST':
        
        email = request.POST['email']
        password = request.POST['password']

        try:
            lawyer = Lawyer.objects.get(email=email)
        except Lawyer.DoesNotExist:
            messages.error(request, "Your account is not approved yet.")
            return redirect('lawyer_login')

        if check_password(password, lawyer.password):
            request.session['lawyer_id'] = lawyer.id
            return redirect('lawyer_dashboard')
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, 'lawyers/login.html')
    

def lawyer_signup(request):
    if request.method == 'POST':
        LawyerRequest.objects.create(
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            password=make_password(request.POST['password']),
            specialization=request.POST['specialization'],
            experience=request.POST['experience'],
            city=request.POST['city'],
            fee=request.POST['fee'],
            about=request.POST['about'],
            documents=request.FILES.get('documents')
        )
        messages.success(request, "Your request has been submitted. Wait for admin approval.")
        return redirect('/')

    return render(request, 'lawyers/signup.html')


def lawyer_dashboard(request):
    lawyer_id = request.session.get('lawyer_id')
    if not lawyer_id:
        return redirect('lawyer_login')

    lawyer = Lawyer.objects.get(id=lawyer_id)
    return render(request, 'lawyers/lawyer_dashboard.html', {'lawyer': lawyer})
   

def lawyer_profile(request):
    lawyer_id=request.session.get('lawyer_id')
    if not lawyer_id:
        return redirect('lawyer_login')
    lawyer=Lawyer.objects.get(id=lawyer_id)
    return render(request, 'lawyers/lawyer_profile.html', {'lawyer': lawyer})

def edit_lawyer_profile(request):

    if not request.session.get("lawyer_id"):
        return redirect("lawyer_login")
    
    lawyer = Lawyer.objects.get(id=request.session["lawyer_id"])

    if request.method == "POST":
        # Get data from form
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        specialization = request.POST.get("specialization")
        experience = request.POST.get("experience")
        fee = request.POST.get("fee")
        about = request.POST.get("about")
        documents = request.FILES.get("documents")
    
        lawyer.full_name = full_name
        lawyer.phone = phone
        lawyer.city = city
        lawyer.specialization = specialization
        lawyer.experience = experience
        lawyer.fee = fee
        lawyer.about = about

        if documents:
                lawyer.documents = documents
        
        lawyer.save()


    return render(request,'lawyers/lawyer_editprofile.html', {"lawyer": lawyer})


def lawyer_change_password(request):

    if not request.session.get("lawyer_id"):
        return redirect("lawyer_login")
    

    lawyer = Lawyer.objects.get(id=request.session["lawyer_id"])
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        
        if not check_password(old_password, lawyer.password):
            messages.error(request, "Old password is incorrect.")
            return redirect('lawyer_change_password')

        
        if new_password != confirm_password:
            messages.error(request, "New password and Confirm password do not match.")
            return redirect('lawyer_change_password')

        
        lawyer.password = make_password(new_password)
        lawyer.save()
        # check=Lawyer.objects.get(id=request.session["lawyer_id"])
        # print(check_password("your_new_password --------->>>>>>>>>>", check.password))

        messages.success(request, "Your password has been updated successfully.")
        return redirect("lawyer_dashboard")


    return render(request,'lawyers/change_password.html')

def lawyer_logout(request):
    
    request.session.flush()
    return redirect('/')



