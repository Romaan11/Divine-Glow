from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, FormView
from django.contrib import messages
from divine_app.forms import AppointmentForm, ContactForm, NewsletterForm    
from django.http import JsonResponse

from divine_app.models import Appointment

# Create your views here.
class HomeView(TemplateView):
    template_name = 'divine/home.html'

class AboutView(TemplateView):
    template_name = 'divine/about.html'


class AppointmentView(FormView):
    template_name = 'divine/appointment.html'
    form_class = AppointmentForm
    success_url = '/appointment/'

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "Successfully reserved appointment."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
        # messages.error(
        #     self.request,
        #     "Can't reserve on the given date and time. Please select another."
        # )
        # return super().form_invalid(form)


# For already booked slots
class BookedSlotsView(View):
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

class ContactView(View):
    template_name = "divine/contact.html"

    def get(self, request):
        return render(request, self.template_name)
    
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
            return redirect("contact") 
            


class NewsletterView(View):
    def post(self,request):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            form = NewsletterForm(request.POST)
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