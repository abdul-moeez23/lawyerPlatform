from django.shortcuts import render
from lawyers.models import LawyerProfile
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.

def search_lawyers(request):
    practice_area = request.GET.get('practice_area')
    city = request.GET.get('city')

    lawyers = LawyerProfile.objects.all()
    if practice_area:
        lawyers = lawyers.filter(practice_areas__name__icontains=practice_area)
    if city:
        lawyers = lawyers.filter(city__name__icontains=city)

    return render(request, 'clients/search_results.html', {'lawyers': lawyers})

def home(request):
    verified_lawyers = LawyerProfile.objects.filter(verification_status='approved').count()
    return render(request, 'clients/index.html', {'verified_lawyers': verified_lawyers})

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        user = authenticate(request, username=email, password=password)
        
        if user:
            login(request, user)
            
           
            if user.role == 'lawyer':
               
                lawyer_profile = LawyerProfile.objects.get(user_id=user.id)
                if lawyer_profile.verification_status == 'approved':
                    return redirect('lawyer_dashboard') 
                else:
                    # return render(request, 'waiting_for_approval.html')
                    return render(request, 'clients/signin.html')
                      
            # else:
            #     return redirect('client_dashboard')  
            
        else:
          
            messages.error(request, "Invalid email or password",extra_tags="auto")
            return redirect('signin')
    

    return render(request, 'clients/signin.html')