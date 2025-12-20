from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import User
from lawyers.models import LawyerProfile

def verify_email(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
        if user.is_email_verified:
             messages.info(request, "Email already verified.")
        else:
            user.is_email_verified = True
            # user.email_verification_token = None # keep token for record or clear it? Better clear to prevent reuse if we wanted one-time but URL is public.
            # Actually, clearing it is safer.
            user.email_verification_token = None
            user.is_active = True 
            user.save()
            messages.success(request, "Email verified successfully!")
        
        # Log user in
        login(request, user)
        
        # Redirect Logic
        if user.role == 'lawyer':
             try:
                 lp = user.lawyer_profile
                 # If profile is not complete, go to complete
                 if lp.verification_status == 'approved':
                      return redirect('lawyer_dashboard')
                 # If pending or empty, go to completion/status page
                 return redirect('lawyer_profile_complete')
             except:
                  return redirect('lawyer_profile_complete')
                  
        elif user.role == 'client':
            return redirect('index') 
        
        else:
            return redirect('/myadmin/')

    except User.DoesNotExist:
        messages.error(request, "Invalid verification token.")
        # redirect to a generic login or home
        return redirect('signin')

def verification_sent(request):
    return render(request, 'users/verification_sent.html')

