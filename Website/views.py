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


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def cookies_policy(request):
    """Display cookie preferences page"""
    return render(request, 'pages/cookies.html')

@require_POST
def save_cookie_preferences(request):
    """Save user's cookie preferences to session"""
    action = request.POST.get('action')
    
    # Initialize cookie preferences in session if not exists
    if 'cookie_preferences' not in request.session:
        request.session['cookie_preferences'] = {
            'necessary': True,  # Always required
            'analytics': False,
            'marketing': False
        }
    
    if action == 'accept_all':
        # Accept all cookies
        request.session['cookie_preferences']['analytics'] = True
        request.session['cookie_preferences']['marketing'] = True
    elif action == 'decline_all':
        # Decline all optional cookies
        request.session['cookie_preferences']['analytics'] = False
        request.session['cookie_preferences']['marketing'] = False
    elif action == 'save_preferences':
        # Save individual preferences
        request.session['cookie_preferences']['analytics'] = 'analytics' in request.POST
        request.session['cookie_preferences']['marketing'] = 'marketing' in request.POST
    
    # Mark that user has set their preferences
    request.session['cookie_preferences_set'] = True
    request.session.modified = True
    
    # Return to the same page or redirect as needed
    return redirect(request.META.get('HTTP_REFERER', '/'))

def some_protected_view(request):
    """Example view that checks cookie preferences"""
    # Check if user has allowed analytics cookies
    analytics_allowed = request.session.get('cookie_preferences', {}).get('analytics', False)
    
    if analytics_allowed:
        # Track analytics here
        pass
        
    return render(request, 'some_template.html')

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
