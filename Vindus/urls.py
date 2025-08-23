"""
URL configuration for Vindus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Website.views import *
from Website.views import case_studies
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('contact/', contact, name='contact'),
    path('careers/', careers, name='careers'),
    path('internship/', internship, name='internship'),
    path('terms-of-use/', terms_of_use, name='terms_of_use'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('cookies/', cookies_policy, name='cookies_policy'),
    path('save-cookie-preferences/', save_cookie_preferences, name='save_cookie_preferences'),
    path('sitemap/', sitemap, name='sitemap'),
    path('case_studies/', sitemap, name='case_studies'),
    path('how_it_works/', sitemap, name='how_it_works'),
    path('login/', admin_login, name='admin_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', admin_logout, name='admin_logout'),
    path('contacts/', contact_list, name='contact_list'),
    path('careerlist/', career_list, name='career_list'),
    path('internships/', internship_list, name='internship_list'),
    path('internship/<int:pk>/', internship_detail, name='internship_detail'),
    path('internship/<int:pk>/edit/', internship_edit, name='internship_edit'),
    path('jobs/', job_list, name='job_list'),
    path('jobs/create/', job_create, name='job_create'),
    path('jobs/<int:pk>/update/', job_update, name='job_update'),
    path('jobs/<int:pk>/delete/', job_delete, name='job_delete'),
    path('case_studies', case_studies, name='case_studies'),
    path('jobs/<int:pk>/apply/', apply_for_job, name='apply_for_job'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
