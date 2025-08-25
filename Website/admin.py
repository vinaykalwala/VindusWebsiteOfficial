from django.contrib import admin
from .models import Contact, CareerApplication, InternshipApplication, Job

admin.site.register(Contact)
admin.site.register(CareerApplication)
admin.site.register(InternshipApplication)
admin.site.register(Job)
