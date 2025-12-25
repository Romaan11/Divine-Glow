from django import forms
from divine_app.models import Appointment,Contact, Newsletter, Service
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class SignupForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'custom-input',
            'autocomplete': 'off', 
            'placeholder': 'Email Address'
        })
    )
    phone = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'custom-input',
            'autocomplete': 'off', 
            'placeholder': 'Phone Number'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'custom-input',
            'autocomplete': 'off', 
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'custom-input',
            'autocomplete': 'off', 
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'custom-input',
            'autocomplete': 'off', 
            'placeholder': 'Confirm Password'
        })
    )

    # Validate phone
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.startswith(('98','97')) or len(phone) != 10 or not phone.isdigit():
            raise ValidationError("Phone must start with 98 or 97 and be exactly 10 digits")
        return phone
    
    # Validate email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValidationError("Enter a valid email address")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered. Please use a different email.")
        return email

    def validate_password_rules(self, password):
        if not password:
            raise ValidationError("Password is required.")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one number.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        self.validate_password_rules(password1)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")

        return cleaned_data


class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'custom-input',
            'placeholder': 'Enter 6-digit OTP',
            'autocomplete': 'off'
        })
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'custom-input',
            'autocomplete': 'off', 
            'placeholder': 'Email Address'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'custom-input',
            'autocomplete': 'off', 
            'placeholder': 'Password'
        })
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None) 
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password")

            self.user = authenticate(
                username=user.username,
                password=password
            )

            if self.user is None:
                raise forms.ValidationError("Invalid email or password")

        return cleaned_data

    def get_user(self):
        return self.user


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
                'pattern': '(98|97)[0-9]{8}',  
                'title': 'Phone no must start with 98 or 97 and be exactly 10 digits'
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
        if not phone:
            raise ValidationError("Phone number is required.")
        if len(phone) != 10 or not phone.startswith(('98', '97')) or not phone.isdigit():
            raise ValidationError("Phone number must start with '98' or '97' and be exactly 10 digits long.")
        return phone
    
    # Validate email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Email is required.")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValidationError("Enter a valid email address.")
        return email
    
    # Validate preferred date and time
    def clean_preferred_date(self):
        date = self.cleaned_data.get("preferred_date")
        if date is None:
            raise ValidationError("Preferred date is required.")
        return date

    def clean_preferred_time(self):
        time = self.cleaned_data.get("preferred_time")
        if time is None:
            raise ValidationError("Preferred time is required.")
        return time


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
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValidationError("Enter a valid email address.")
        return email


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = "__all__"

