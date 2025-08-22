from django import forms
from .models import Contact, CareerApplication, InternshipApplication

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']

class CareerForm(forms.ModelForm):
    class Meta:
        model = CareerApplication
        fields = ['name', 'email', 'phone', 'resume', 'message']

class InternshipForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        exclude = [
            'batch_assigned',
            'internship_type',
            'interview_score',
            'applied_at',
            'status',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'prior_experience': forms.Textarea(attrs={'rows': 3}),
            'why_choose': forms.Textarea(attrs={'rows': 3}),
            'expectations': forms.Textarea(attrs={'rows': 3}),
            'career_goals': forms.Textarea(attrs={'rows': 3}),
            'message': forms.Textarea(attrs={'rows': 3}),
            'agreement_accepted': forms.CheckboxInput(),
            'device_access': forms.CheckboxInput(),
        }

    def clean_agreement_accepted(self):
        """Ensure the applicant has accepted terms and conditions."""
        agreement = self.cleaned_data.get('agreement_accepted')
        if not agreement:
            raise forms.ValidationError("You must accept the terms and conditions to proceed.")
        return agreement
    
from django import forms
from .models import InternshipApplication

class InternshipApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        # Include only fields that admin can edit
        fields = [
            'name', 'profile_photo','email', 'phone', 'qualification', 'specialization', 'college', 'university',
            'graduation_year', 'aggregate_percentage', 'skills', 'prior_experience',
            'why_choose', 'expectations', 'career_goals', 'device_access',
            'resume', 'cover_letter', 'college_id_card',
            'emergency_contact_name', 'emergency_contact_phone', 'guardian_name', 'guardian_contact',
            'linkedin_profile', 'portfolio_link', 'reference',
            'batch_assigned', 'internship_type', 'interview_score', 'message', 'agreement_acceptance', 'status'
        ]
