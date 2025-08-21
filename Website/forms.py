from django import forms
from .models import Contact, CareerApplication, InternshipApplication

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

class CareerForm(forms.ModelForm):
    class Meta:
        model = CareerApplication
        fields = ['name', 'email', 'phone', 'resume', 'message']

class InternshipForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        fields = ['name', 'email', 'phone', 'course', 'college', 'resume', 'message']
