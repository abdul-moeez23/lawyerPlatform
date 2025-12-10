from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# from .models import User
from lawyers.models import LawyerProfile
from django.contrib.auth.hashers import make_password,check_password
from users.models import User,City, Court, Language, FeeBand,SubCategory
from lawyers.models import VerificationDocument






def lawyer_login(request):
    # storage = messages.get_messages(request)
    # storage.used = True
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password",extra_tags="auto")
            return redirect("lawyer_login")

        if user.role != "lawyer":
            messages.error(request, "This account is not registered as a lawyer",extra_tags="auto")
            return redirect("lawyer_login")

        # verification check
        try:
            lp = user.lawyer_profile
        except LawyerProfile.DoesNotExist:
            messages.error(request, "Complete your profile first")
            return redirect("lawyer_profile_complete")

        if lp.verification_status == "pending":
            messages.info(request, "Your profile is pending verification")
            # return redirect("waiting_verification")
            # return redirect("lawyer_dashboard")
            return redirect("lawyer_login") 

        if lp.verification_status == "rejected":
            messages.error(request, "Your profile was rejected. Contact admin.")
            return redirect("lawyer_profile_complete")

        # if verified
        if lp.verification_status == "approved":
            print("Verified")   
            login(request, user)
            return redirect("lawyer_dashboard")
        if lp.verification_status == '':
            login(request, user)
            return redirect("lawyer_dashboard")

    return render(request, "lawyers/login.html")




def lawyer_signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # Check existing user
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect("lawyer_signup")

        # Create User
        user = User.objects.create(
            username=email,
            email=email,
            first_name=name,
            phone=phone,
            role='lawyer',
            password=make_password(password),
        )

        # Create empty lawyer profile
        LawyerProfile.objects.create(
            user=user,
            verification_status=''
        )

        messages.success(request, "Signup successful. Admin will verify your account",extra_tags='auto')
        login(request, user)
        return redirect("lawyer_profile_complete")

    return render(request, "lawyers/signup.html")



def lawyer_profile_complete(request):
    if request.method == "POST":

        lp = LawyerProfile.objects.get(user=request.user)

        lp.bar_enrollment = request.POST.get("bar_enrollment")
        lp.city_id = request.POST.get("city")
        lp.fee_band_id = request.POST.get("fee_band")
        lp.experience_years = request.POST.get("experience")
        if request.FILES.get('profile_picture'):
            lp.profile_picture = request.FILES['profile_picture']
        lp.verification_status = 'pending'
        
        lp.save()

        courts_ids = request.POST.getlist("courts")
        # languages_ids = request.POST.getlist("languages")
        practice_ids = request.POST.getlist("practice_areas")

        lp.courts.set(courts_ids)
        # lp.languages.set(languages_ids)
        lp.practice_areas.set(practice_ids)

        # Handle verification documents upload

        from lawyers.models import VerificationDocument
        files = request.FILES.getlist('verification_documents')
        for file in files:
            VerificationDocument.objects.create(
                lawyer=lp,
                file=file
            )
        
        
        # LawyerProfile.objects.create(
        # #     user=user,
        #     verification_status='pending'
        # )

        # request.user.profile_completed = True
        request.user.save()
        messages.success(request, "Profile completed successfully")
        return redirect('lawyer_login')



    from users.models import City, Court, SubCategory, FeeBand, Language
    
    context = {
        'cities': City.objects.all(),
        'fee_bands': FeeBand.objects.all(),
        'courts': Court.objects.all(),
        'languages': Language.objects.all(),
        'practice_areas': SubCategory.objects.all(),
    }
    
    return render(request, "lawyers/profile_complete.html", context)


def waiting_verification(request):
    return render(request, "lawyers/waiting.html")

@login_required(login_url='/lawyer/lawyer-login/')
def lawyer_dashboard(request):
    
    lawyer = request.user  # session se automatic fetch
    return render(request, 'lawyers/lawyer_dashboard.html', {'lawyer': lawyer})


def lawyer_profile(request):
    # lawyer = request.user
    lawyer_profile = get_object_or_404(LawyerProfile, user=request.user)
    return render(request, 'lawyers/lawyer_profile.html', {'lawyer': lawyer_profile})






# def lawyer_login(request):

#     if request.method == 'POST':
        
#         email = request.POST['email']
#         password = request.POST['password']

#         try:
#             lawyer = Lawyer.objects.get(email=email)
#         except Lawyer.DoesNotExist:
#             messages.error(request, "Your account is not approved yet.")
#             return redirect('lawyer_login')

#         if check_password(password, lawyer.password):
#             request.session['lawyer_id'] = lawyer.id
#             return redirect('lawyer_dashboard')
#         else:
#             messages.error(request, "Invalid credentials.")
    
#     return render(request, 'lawyers/login.html')
    



# def lawyer_signup(request):
#     if request.method == 'POST':
#         LawyerRequest.objects.create(
#             full_name=request.POST['full_name'],
#             email=request.POST['email'],
#             phone=request.POST['phone'],
#             password=make_password(request.POST['password']),
#             specialization=request.POST['specialization'],
#             experience=request.POST['experience'],
#             city=request.POST['city'],
#             fee=request.POST['fee'],
#             about=request.POST['about'],
#             documents=request.FILES.get('documents')
#         )
#         messages.success(request, "Your request has been submitted. Wait for admin approval.")
#         return redirect('/')

#     return render(request, 'lawyers/signup.html')


# def lawyer_dashboard(request):
#     lawyer_id = request.session.get('lawyer_id')
#     if not lawyer_id:
#         return redirect('lawyer_login')

#     lawyer = Lawyer.objects.get(id=lawyer_id)
#     return render(request, 'lawyers/lawyer_dashboard.html', {'lawyer': lawyer})
   

# def lawyer_profile(request):
#     lawyer_id=request.session.get('lawyer_id')
#     if not lawyer_id:
#         return redirect('lawyer_login')
#     lawyer=Lawyer.objects.get(id=lawyer_id)
#     return render(request, 'lawyers/lawyer_profile.html', {'lawyer': lawyer})


# def edit_lawyer_profile(request):
#     if not request.user.is_authenticated:
#         return redirect("lawyer_login")

#     lawyer = request.user
#     return render(request,'lawyers/lawyer_editprofile.html')

@login_required(login_url='/lawyer/lawyer-login/')
def edit_lawyer_profile(request):

    user = request.user
    lawyer_profile = LawyerProfile.objects.get(user=user)

    if request.method == "POST":

        # ========== BASIC INFO ==========
        user.first_name = request.POST.get("first_name")
        user.phone = request.POST.get("phone")
        user.save()

        # ========== LAWYER PROFILE FIELDS ==========
        lawyer_profile.city_id = request.POST.get("city")
        lawyer_profile.experience_years = request.POST.get("experience")
        lawyer_profile.fee_band_id = request.POST.get("fee_band")

        # ========== PROFILE PICTURE ==========
        if request.FILES.get('profile_picture'):
            lawyer_profile.profile_picture = request.FILES['profile_picture']

        # ========== CHECKBOX MULTIPLE FIELDS ==========
        selected_courts = request.POST.getlist("courts")
        selected_languages = request.POST.getlist("languages")
        selected_practice_areas = request.POST.getlist("practice_areas")

        # Clear previous selections
        lawyer_profile.courts.clear()
        # lawyer_profile.languages.clear()
        lawyer_profile.practice_areas.clear()

        # Add new checked ones
        if selected_courts:
            lawyer_profile.courts.add(*selected_courts)

        if selected_languages:
            lawyer_profile.languages.add(*selected_languages)

        if selected_practice_areas:
            lawyer_profile.practice_areas.add(*selected_practice_areas)

        # ========== DOCUMENTS ==========
        document_file = request.FILES.get("documents")
        if document_file:
            lawyer_profile.verificationdocument_set.create(file=document_file)

        lawyer_profile.save()

        return redirect("lawyer_dashboard")

    # ========== DATA FOR TEMPLATE ==========
    cities = City.objects.all()
    courts = Court.objects.all()
    languages = Language.objects.all()
    practice_areas = SubCategory.objects.all()
    fee_bands = FeeBand.objects.all()

    return render(request, 'lawyers/lawyer_editprofile.html', {
        "user": user,
        "lawyer": lawyer_profile,
        "cities": cities,
        "courts": courts,
        "languages": languages,
        "practice_areas": practice_areas,
        "fee_bands": fee_bands,
    })

# def lawyer_change_password(request):
#     return render(request,'lawyers/change_password.html')

# # @login_required(login_url='/login/')

@login_required(login_url='/lawyer/lawyer-login/')
def lawyer_change_password(request):

    lawyer = request.user   # login user (session se auto ata ha)

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # 1. Check old password correct?
        if not check_password(old_password, lawyer.password):
            messages.error(request, "Old password is incorrect.")
            return redirect('lawyer_change_password')

        # 2. New passwords match?
        if new_password != confirm_password:
            messages.error(request, "New password and Confirm password do not match.")
            return redirect('lawyer_change_password')

        # 3. Update password securely
        lawyer.password = make_password(new_password)
        lawyer.save()

        messages.success(request, "Your password has been updated successfully.")
        return redirect('lawyer_dashboard')

    return render(request, 'lawyers/change_password.html')
# def lawyer_logout(request):
    
#     request.session.flush()
#     return redirect('/')

def lawyer_logout(request):
    logout(request)
    return redirect('/')    

