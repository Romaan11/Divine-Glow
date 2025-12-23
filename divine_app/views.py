from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, FormView, ListView
from django.contrib import messages
from divine_app.forms import LoginForm, Service, AppointmentForm, ContactForm, NewsletterForm, SignupForm    
from django.http import JsonResponse
from divine_app.models import Appointment, Newsletter

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class UserSignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')



class HomeView(TemplateView):
    template_name = 'divine/home.html'

class AboutView(TemplateView):
    template_name = 'divine/about.html'

class ServiceView(ListView):
    model = Service
    template_name = 'divine/service.html'
    context_object_name = 'services'
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Service.objects.all()
        if self.request.GET.get('all'):
            return qs
        return qs[:8]

class AppointmentView(LoginRequiredMixin, FormView):
    template_name = 'divine/appointment.html'
    form_class = AppointmentForm
    success_url = '/appointment/'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        service_id = self.request.GET.get('service')

        # ONLY when coming from service page
        if service_id:
            service = get_object_or_404(Service, id=service_id)
            form.fields['service'].initial = service
            form.fields['service'].disabled = True
        else:
            # Direct visit → no pre-selected service
            form.fields['service'].initial = None

        return form

    def form_valid(self, form):
        service_id = self.request.GET.get('service')

        if service_id:
            service = get_object_or_404(Service, id=service_id)
            form.instance.service = service

        form.save()
        messages.success(
            self.request,
            "Successfully reserved appointment."
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locked_service'] = bool(self.request.GET.get('service'))
        return context


# For already booked slots
class BookedSlotsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        appointments = Appointment.objects.values(
            'preferred_date', 'preferred_time'
        )

        data = {}
        for appt in appointments:
            date = appt['preferred_date'].strftime('%Y-%m-%d')
            time = appt['preferred_time'].strftime('%H:%M')
            data.setdefault(date, []).append(time)

        return JsonResponse(data)

class ContactView(LoginRequiredMixin, View):
    template_name = "divine/contact.html"
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Successfully submitted your query. We will contact you soon."
            )
            return redirect("contact")
        else:
            messages.error(
                request, "Cannot submit your query. Please make sure all fields are valid.",
            )
            return render(request, self.template_name, {'form': form})
            


class NewsletterView(View):
    def post(self,request):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            form = NewsletterForm(request.POST)

            email = request.POST.get("email")
            
            if Newsletter.objects.filter(email=email).exists():
                return JsonResponse(
                    {
                        "success": False,
                        "message": "You have already subscribed to the newsletter.",
                    },
                    status=400,
                )

            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                    "success": True,
                    "message": "Successfully subscribed to the newsletter.",
                    },
                    status=201,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot subscribe to the newsletter.",
                    },
                    status=400,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process. Must be an AJAX XMLHttpRequest",
                },
                status=400,
            )