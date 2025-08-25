from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15,blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class CareerApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    message = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms

class InternshipApplication(models.Model):
    # Basic Personal Information
    name = models.CharField(max_length=100)
    profile_photo = models.ImageField(
        upload_to='internships/profile_photos/',
        blank=True,
        null=True,
        help_text="Upload your profile photo"
    )
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True
    )
    address = models.TextField(blank=True)

    # Academic Information
    qualification = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True)
    college = models.CharField(max_length=150)
    university = models.CharField(max_length=150, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    aggregate_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Overall percentage (0–100, up to 2 decimals)"
    )

    # Skills & Experience
    skills = models.TextField(help_text="List your technical and soft skills")
    prior_experience = models.TextField(blank=True, help_text="Any previous internship or work experience")

    # Internship-Specific Questions
    why_choose = models.TextField(help_text="Why are you interested in this internship?")
    expectations = models.TextField(help_text="What do you expect to gain from this internship?")
    career_goals = models.TextField(help_text="Where do you see yourself in the next 2–3 years?")
    device_access = models.BooleanField(default=False, help_text="Do you have a laptop or PC for the internship?")

    # Documents
    resume = models.FileField(upload_to='internships/resumes/')
    cover_letter = models.FileField(upload_to='internships/cover_letters/', blank=True, null=True)
    college_id_card = models.FileField(upload_to='internships/id_cards/', blank=True, null=True)

    # Emergency & Guardian Details
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_contact = models.CharField(max_length=15, blank=True)

    # Professional Links
    linkedin_profile = models.URLField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, help_text="How did you hear about us?")

    # Administrative Fields
    batch_assigned = models.CharField(max_length=100, blank=True)
    internship_type = models.CharField(
        max_length=50,
        choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')],
        default='Paid'
    )
    interview_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Other Fields
    message = models.TextField(blank=True)
    agreement_acceptance = models.BooleanField(default=False, help_text="Agree to all terms and conditions?")
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Reviewed', 'Reviewed'),
            ('Shortlisted', 'Shortlisted'),
            ('Rejected', 'Rejected'),
            ('Selected', 'Selected')
        ],
        default='Pending'
    )

    def __str__(self):
        return f"{self.name} - {self.qualification}"

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class JobOpening(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    employment_type = models.CharField(
        max_length=50,
        choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Internship', 'Internship')],
        default='Full-Time'
    )
    required_qualification = models.CharField(max_length=200, blank=True)
    skills_required = models.TextField(blank=True)
    experience_required = models.TextField(blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True
    )
    address = models.TextField(blank=True)
    qualification = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True)
    aggregate_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    skills = models.TextField(help_text="Technical and soft skills")
    prior_experience = models.TextField(blank=True)
    resume = models.FileField(upload_to='job_applications/resumes/')
    cover_letter = models.FileField(upload_to='job_applications/cover_letters/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Reviewed', 'Reviewed'),
            ('Shortlisted', 'Shortlisted'),
            ('Rejected', 'Rejected'),
            ('Selected', 'Selected')
        ],
        default='Pending'
    )
    agreement_acceptance = models.BooleanField(default=False, help_text="Agree to all terms and conditions?")

    def __str__(self):
        return f"{self.name} - {self.job.title}"
