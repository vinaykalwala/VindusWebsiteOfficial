from django.shortcuts import render, redirect
from .forms import ContactForm, CareerForm, InternshipForm
from .models import Contact, CareerApplication, InternshipApplication

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

def how_it_works(request):
    return render(request,'pages/howitworks.html')

def why_choose_us(request):
    return render(request,'pages/whychooseus.html')


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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import JobOpening, CareerApplication, JobApplication
from .forms import CareerForm, JobApplicationForm

def careers(request):
    jobs = JobOpening.objects.filter(is_active=True).order_by('-posted_at')

    if request.method == "POST":
        # Determine which form is submitted
        if 'job_id' in request.POST:
            # Job application form submitted
            form = JobApplicationForm(request.POST, request.FILES)
            job_id = request.POST.get('job_id')
            job = get_object_or_404(JobOpening, id=job_id)
            if form.is_valid():
                application = form.save(commit=False)
                application.job = job
                application.save()
                messages.success(request, f"Your application for {job.title} has been submitted!")
                return redirect('careers')
            else:
                messages.error(request, "Please fill all required fields correctly for the job application.")
        else:
            # General profile form submitted
            form = CareerForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile has been submitted successfully!")
                return redirect('careers')
            else:
                messages.error(request, "Please fill all required fields correctly for your profile.")
    else:
        form = CareerForm()
        job_form = JobApplicationForm()

    return render(request, 'pages/careers.html', {
        'jobs': jobs,
        'form': form,
        'job_form': JobApplicationForm()
    })

from django.shortcuts import render

def case_studies(request):
    return render(request, "pages/case_studies.html")



from django.shortcuts import render
from django.views.generic import TemplateView

class ProductsView(TemplateView):
    template_name = 'pages/products.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Product data that can be passed to the template
        context['products'] = [
            {
                'number': 1,
                'name': 'QTipStore',
                'tagline': 'Smart & Scalable E-Commerce Platform',
                'for_text': 'Retailers, B2B & B2C Businesses, Entrepreneurs',
                'features': [
                    'Customizable Online Store – Fully responsive and tailored to your brand',
                    'Secure Payment Gateway – Supports multiple payment methods',
                    'AI-Based Product Recommendations – Enhances customer shopping experience',
                    'Inventory & Order Management – Real-time stock tracking',
                    'Multi-Vendor Support – Manage multiple sellers on one platform'
                ],
                'cta': 'Grow your business online with QTipStore!',
                'link_text': 'Visit QTipStore'
            },
            {
                'number': 2,
                'name': 'VAudit',
                'tagline': 'Powerful SEO & Website Analysis Tool',
                'for_text': 'Digital Marketers, SEO Experts, Website Owners',
                'features': [
                    'Comprehensive SEO Audit – Identify technical issues',
                    'Keyword & Competitor Research – Gain insights to rank higher',
                    'On-Page & Off-Page Optimization – Actionable recommendations',
                    'Real-Time Monitoring – Track traffic and backlinks',
                    'Automated Reports & Suggestions – AI-powered analysis'
                ],
                'cta': 'Boost your website\'s performance with VAudit!',
                'link_text': 'Try VAudit Now'
            },
            {
                'number': 3,
                'name': 'VOrbit',
                'tagline': 'Advanced Business & Employee Management Tool',
                'for_text': 'Startups, Enterprises, HR Teams, Project Managers',
                'features': [
                    'Attendance & Break Management – Track employee work hours',
                    'Client & User Management – Organize interactions and permissions',
                    'Portfolio Generation – Create professional employee portfolios',
                    'Asset & Leave Tracking – Manage company assets and time off',
                    'Email Login Integration – Secure authentication system'
                ],
                'cta': 'Streamline your business operations with VOrbit!',
                'link_text': 'Explore VOrbit'
            },
            {
                'number': 4,
                'name': 'Case Management Solutions',
                'tagline': 'Streamlining Legal Workflows',
                'for_text': 'Law Firms, Legal Advisors, Corporate Legal Teams',
                'features': [
                    'Case & Client Management – Organize legal records seamlessly',
                    'Automated Legal Research – AI-powered insights',
                    'Document Storage & Security – Cloud-based access to files',
                    'Billing & Invoicing – Simplifies legal fee management',
                    'Appointment & Scheduling – Manage meetings efficiently'
                ],
                'cta': 'Enhance legal operations with our solutions!',
                'link_text': 'Request a Demo'
            }
        ]
        return context
    

from django.shortcuts import render, get_object_or_404, redirect
from .models import JobOpening, JobApplication
from .forms import JobApplicationForm


# Job details page
def job_detail(request, job_id):
    job = get_object_or_404(JobOpening, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

# Apply for a specific job
def apply_job(request, job_id):
    job = get_object_or_404(JobOpening, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            return render(request, 'application_success.html', {'job': job})
    else:
        form = JobApplicationForm()
    return render(request, 'apply_job.html', {'form': form, 'job': job})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import JobOpening, JobApplication
from .forms import JobOpeningForm, JobApplicationForm

# ===============================
# JobOpening Views
# ===============================

def job_list(request):
    jobs = JobOpening.objects.all().order_by('-posted_at')
    return render(request, 'job_list.html', {'jobs': jobs})

def job_create(request):
    if request.method == "POST":
        form = JobOpeningForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job opening created successfully!")
            return redirect('job_list')
    else:
        form = JobOpeningForm()
    return render(request, 'job_form.html', {'form': form, 'title': 'Add Job Opening'})

def job_edit(request, job_id):
    job = get_object_or_404(JobOpening, id=job_id)
    if request.method == "POST":
        form = JobOpeningForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job opening updated successfully!")
            return redirect('job_list')
    else:
        form = JobOpeningForm(instance=job)
    return render(request, 'job_form.html', {'form': form, 'title': 'Edit Job Opening'})

def job_delete(request, job_id):
    job = get_object_or_404(JobOpening, id=job_id)
    job.delete()
    messages.success(request, "Job opening deleted successfully!")
    return redirect('job_list')

# ===============================
# JobApplication Views
# ===============================

def application_list(request):
    status_filter = request.GET.get('status')
    applications = JobApplication.objects.all().order_by('-applied_at')
    if status_filter:
        applications = applications.filter(status=status_filter)
    return render(request, 'application_list.html', {'applications': applications, 'status_filter': status_filter})

def application_edit(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Application updated successfully!")
            return redirect('application_list')
    else:
        form = JobApplicationForm(instance=application)
    return render(request, 'application_form.html', {'form': form, 'title': 'Edit Job Application'})

def application_delete(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    application.delete()
    messages.success(request, "Application deleted successfully!")
    return redirect('application_list')
