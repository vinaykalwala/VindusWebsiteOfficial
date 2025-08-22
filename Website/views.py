from django.shortcuts import render, redirect
from .models import Contact, CareerApplication, InternshipApplication
from .forms import ContactForm, CareerForm, InternshipForm

def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def services(request):
    return render(request, 'pages/services.html')

def terms_of_use(request):
    return render(request, 'pages/termsofuse.html')

def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')

def cookies_policy(request):
    return render(request, 'pages/cookies.html')

def sitemap(request):
    return render(request, 'pages/sitemap.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')  # Or redirect to a success page
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})


def careers(request):
    if request.method == "POST":
        form = CareerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('careers')
    else:
        form = CareerForm()
    return render(request, 'pages/careers.html', {'form': form})

def internship(request):
    if request.method == "POST":
        form = InternshipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('internship')
    else:
        form = InternshipForm()
    return render(request, 'pages/internship.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Contact, CareerApplication, InternshipApplication
from .forms import InternshipApplicationForm  # Form for editing internship applicants

# Decorator to allow only superusers
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_active and u.is_superuser)(view_func)

# Login
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized.')
    return render(request, 'admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('home')

@superuser_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Contact List
@superuser_required
def contact_list(request):
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'contact_list.html', {'contacts': contacts})

# Career List
@superuser_required
def career_list(request):
    careers = CareerApplication.objects.all().order_by('-applied_at')
    return render(request, 'career_list.html', {'careers': careers})

# Internship List with filters
@superuser_required
def internship_list(request):
    qs = InternshipApplication.objects.all().order_by('-applied_at')

    # Filtering
    status = request.GET.get('status')
    batch = request.GET.get('batch')
    name = request.GET.get('name')
    internship_type = request.GET.get('internship_type')

    if status:
        qs = qs.filter(status__icontains=status)
    if batch:
        qs = qs.filter(batch_assigned__icontains=batch)
    if name:
        qs = qs.filter(name__icontains=name)
    if internship_type:
        qs = qs.filter(internship_type__icontains=internship_type)

    return render(request, 'internship_list.html', {'internships': qs})

# Internship Detail
@superuser_required
def internship_detail(request, pk):
    applicant = get_object_or_404(InternshipApplication, pk=pk)
    return render(request, 'internship_detail.html', {'applicant': applicant})

# Internship Edit
@superuser_required
def internship_edit(request, pk):
    applicant = get_object_or_404(InternshipApplication, pk=pk)
    if request.method == 'POST':
        form = InternshipApplicationForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Applicant updated successfully.')
            return redirect('internship_list')
    else:
        form = InternshipApplicationForm(instance=applicant)
    return render(request, 'internship_edit.html', {'form': form})


