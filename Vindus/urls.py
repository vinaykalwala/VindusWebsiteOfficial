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
    path('login/', admin_login, name='admin_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', admin_logout, name='admin_logout'),
    path('contacts/', contact_list, name='contact_list'),
    path('careerlist/', career_list, name='career_list'),
    path('internships/', internship_list, name='internship_list'),
    path('internship/<int:pk>/', internship_detail, name='internship_detail'),
    path('internship/<int:pk>/edit/', internship_edit, name='internship_edit'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
