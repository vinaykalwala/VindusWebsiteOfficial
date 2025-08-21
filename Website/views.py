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
