from django.utils import timezone
from datetime import time
from django import forms
from divine_app.models import Appointment,Contact, Newsletter, Service
from django.core.exceptions import ValidationError
import re

class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white',
                'placeholder': 'Phone No.',
                'maxlength': '10',
                'pattern': '98[0-9]{8}',  
                'title': 'Phone number must start with 98 and be exactly 10 digits'
            }),
            'preferred_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control py-3 border-white bg-transparent',
                'placeholder': 'Select Date'
            }),
            'preferred_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control py-3 border-white bg-transparent text-white',
            }),
            'service': forms.Select(attrs={
                'class': 'form-select py-3 border-white bg-transparent',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control border-white bg-transparent text-white',
                'rows': 5,
                'placeholder': 'Write your message here...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # Dynamically load services from the database
        self.fields['service'].queryset = Service.objects.all()    
        self.fields['service'].empty_label = "Select Service"

    # Validate phone number
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        # Check if the phone number is exactly 10 digits, starts with '98' or '97', and contains only digits
        if len(phone) != 10 or not phone.startswith(('98', '97')) or not phone.isdigit():
            raise ValidationError(
                "Phone number must start with '98' or '97' and be exactly 10 digits long."
            )

        return phone


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

    # Validate phone number
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        # Validate phone number to ensure it starts with 97 or 98 and is exactly 10 digits long.
        if len(phone) != 10 or not phone.startswith(('98', '97')) or not phone.isdigit():
            raise ValidationError(
                "Phone number must start with '98' or '97' and be exactly 10 digits long."
            )
        return phone
    
    # Email validation using regex
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValidationError("Enter a valid email address.")
        return email


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = "__all__"

