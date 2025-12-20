from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from lawyers.models import LawyerProfile
from .models import Case, CaseDocument, Interaction, Message
from users.models import City, SubCategory


def search_lawyers(request):
    practice_area = request.GET.get('practice_area')
    city = request.GET.get('city')

    lawyers = LawyerProfile.objects.filter(verification_status='approved')
    if practice_area:
        lawyers = lawyers.filter(practice_areas__name__icontains=practice_area)
    if city:
        lawyers = lawyers.filter(city__name__icontains=city)

    return render(request, 'clients/search_results.html', {'lawyers': lawyers})


def home(request):
    # verified_lawyers = LawyerProfile.objects.filter(verification_status='approved').count()
    verified_lawyers = 120 # Mock count or fetch real
    return render(request, 'clients/index.html', {'verified_lawyers': verified_lawyers})


def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user:
            login(request, user)
            
            if user.role == 'lawyer':
                try:
                    lawyer_profile = user.lawyer_profile
                    if lawyer_profile.verification_status == 'approved':
                        return redirect('lawyer_dashboard') 
                    else:
                        return redirect('lawyer_dashboard') # Or waiting page
                except LawyerProfile.DoesNotExist:
                     return redirect('lawyer_profile_complete')
            
            elif user.role == 'client':
                return redirect('client_dashboard')
            
            else: # Admin
                 return redirect('/myadmin/')
            
        else:
            messages.error(request, "Invalid email or password", extra_tags="auto")
            return redirect('signin')

    return render(request, 'clients/signin.html')


# ==========================================
# CLIENT DASHBOARD VIEWS
# ==========================================

# @login_required(login_url='signin')
# @never_cache

def client_dashboard(request):
    # user = request.user
    # if user.role != 'client':
    #     return redirect('signin')

    # # Stats
    # total_cases = Case.objects.filter(client=user).count()
    # active_cases = Case.objects.filter(client=user).exclude(status='closed').count()
    
    # # Logic for hired lawyers (Count cases where status is 'hired')
    # hired_count = Case.objects.filter(client=user, status='hired').count()

    # # Recent Activity (Mix of created cases and interactions) - Simplified for now
    # recent_cases = Case.objects.filter(client=user).order_by('-updated_at')[:3]

    # context = {
    #     'total_cases': total_cases,
    #     'active_cases': active_cases,
    #     'hired_count': hired_count,
    #     'recent_cases': recent_cases,
    # }
    # return render(request, 'clients/dashboard_home.html', context)
    return render(request, 'clients/dashboard_home.html')


# @login_required(login_url='signin')
# @never_cache
def my_cases(request):
    # user = request.user
    # cases = Case.objects.filter(client=user).order_by('-created_at')
    # return render(request, 'clients/my_cases.html', {'cases': cases})
    return render(request, 'clients/my_cases.html')


# @login_required(login_url='signin')
# @never_cache
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk, client=request.user)
    
    # Handle Document Upload
    # if request.method == "POST" and request.FILES.get('document'):
    #     doc_file = request.FILES['document']
    #     doc_title = request.POST.get('title', doc_file.name)
    #     CaseDocument.objects.create(case=case, file=doc_file, title=doc_title)
    #     messages.success(request, "Document uploaded successfully.")
    #     return redirect('case_detail', pk=pk)

    # interactions = Interaction.objects.filter(case=case)
    # documents = CaseDocument.objects.filter(case=case).order_by('-uploaded_at')
    
    # # Chat Logic (Basic: Get messages for this case)
    # chat_messages = Message.objects.filter(case=case).order_by('created_at')

    # context = {
    #     'case': case,
    #     'interactions': interactions,
    #     'documents': documents,
    #     'chat_messages': chat_messages,
    # }
    # return render(request, 'clients/case_detail.html', context)

    return render(request, 'clients/case_detail.html')


# @login_required(login_url='signin')
# @never_cache
def client_profile(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone = request.POST.get('phone')
        # Handle password change separately or here if simple
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('client_profile')

    return render(request, 'clients/profile.html', {'user': user})
