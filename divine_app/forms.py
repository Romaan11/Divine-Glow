from django.utils import timezone
from datetime import time
from django import forms
from divine_app.models import Appointment,Contact, Newsletter
from django.core.exceptions import ValidationError

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
                'placeholder': 'Phone No.'
            }),
            'preferred_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control py-3 border-white bg-transparent'
            }),
            'preferred_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control py-3 border-white bg-transparent text-white'
            }),
            'service': forms.Select(attrs={
                'class': 'form-select py-3 border-white bg-transparent'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control border-white bg-transparent text-white',
                'rows': 5,
                'placeholder': 'Write Comments'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("preferred_date")
        time_value = cleaned_data.get("preferred_time")

        # Validate that the date is not in the past
        if date and date < timezone.now().date():
            raise ValidationError(
                "You cannot select a past date."
            )
        
        # Closed on Friday
        if date and date.weekday() == 4:
            raise ValidationError("We are closed on Fridays.")
        
        # Working hours
        if time_value:
            if not (time(9, 0) <= time_value <= time(22, 0)):
                raise ValidationError(
                    "Appointments are available between 9:00 AM and 10:00 PM."
                )

        # Duplicate booking
        if date and time_value:
            if Appointment.objects.filter(
                preferred_date=date,
                preferred_time=time_value   
            ).exists():
                raise ValidationError(
                    "Can't reserve on the given date and time. Please select another."
                )

        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = "__all__"

