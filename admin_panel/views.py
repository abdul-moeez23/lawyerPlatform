from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from lawyers.models import LawyerRequest,Lawyer

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Django built-in authentication uses username, so agar email use kar rahe ho:
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None and user.is_staff:  # check if user is admin/staff
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not an admin!")
            return redirect('admin_login')

    return render(request, 'admin_panel/login.html')




@login_required
def admin_dashboard(request):
    total_lawyers = Lawyer.objects.count()
    pending_requests = LawyerRequest.objects.count()

    context = {
        'total_lawyers': total_lawyers,
        'pending_requests': pending_requests
    }
    return render(request, 'admin_panel/dashboard.html', context)



def admin_logout(request):
    logout(request)
    return redirect('/')




def pending_lawyer_requests(request):
    requests = LawyerRequest.objects.all().order_by('-submitted_at')
    return render(request, 'admin_panel/pending_lawyers.html', {'requests': requests})


def approve_lawyer(request, id):
    req = LawyerRequest.objects.get(id=id)

    Lawyer.objects.create(
        full_name=req.full_name,
        email=req.email,
        phone=req.phone,
        password=req.password,
        specialization=req.specialization,
        experience=req.experience,
        city=req.city,
        fee=req.fee,
        about=req.about,
        documents=req.documents
    )

    req.delete()

    messages.success(request, "Lawyer approved successfully!")
    return redirect('pending_lawyer_requests')


def approved_lawyers(request):
    lawyer=Lawyer.objects.all().order_by('-created_at')
    return render(request,'admin_panel/approved_lawyers.html',{'lawyers':lawyer})