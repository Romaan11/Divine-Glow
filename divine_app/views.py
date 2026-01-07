from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, FormView, ListView, CreateView, DetailView
from django.contrib import messages
from django import forms 
from divine_app.forms import FeedBackForm, LoginForm, Service, AppointmentForm, ContactForm, NewsletterForm, SignupForm, OTPForm    
from django.http import JsonResponse, HttpResponseNotAllowed
from divine_app.models import Category, Review, UserProfile, Appointment, Newsletter, FeedBack, Product

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.core.mail import send_mail
from django.contrib.auth import logout

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    # success_url = reverse_lazy('home')
    redirect_authenticated_user = True

    # def form_valid(self, form):
    #     login(self.request, form.get_user())
    #     return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('home')

    def form_valid(self, form):
        # Login user after successful authentication
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):  
        # Redirect to home after successful login
        return reverse_lazy('home')

class UserSignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('verify_otp')

    def form_valid(self, form):
        # Save data temporarily in session
        self.request.session['signup_data'] = form.cleaned_data

        # Generate OTP
        otp = random.randint(100000, 999999)
        self.request.session['signup_otp'] = otp

        # Send OTP via SMS or Email
        send_mail(
            subject='Your OTP for Divine Glow Signup',
            message=f'Your OTP is {otp}',
            from_email="no-reply@yourdomain.com",
            recipient_list=[form.cleaned_data['email']]
        )
        
        return redirect('verify_otp')


class OTPVerifiyView(FormView):
    template_name = 'registration/verify_otp.html'
    form_class = OTPForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        session_otp = self.request.session.get('signup_otp')
        entered_otp = form.cleaned_data.get('otp')

        if not session_otp:
            form.add_error(None, "OTP expired. Please sign up again.")
            return self.form_invalid(form)

        if str(session_otp) != entered_otp:
            form.add_error('otp', 'Invalid OTP. Please enter the correct OTP.')
            return self.form_invalid(form)

        # Get signup data from session
        data = self.request.session.get('signup_data')

        # Create or get user
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={'email': data['email']}
        )

        if created:
            # Set password for new user
            user.set_password(data['password1'])
            user.save()

        # Create or get user profile (prevents duplicate)
        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'username': data['username'],
                'email': data['email'],
                'phone': data['phone']
            }
        )

        # Cleanup session
        self.request.session.pop('signup_otp', None)
        self.request.session.pop('signup_data', None)

        messages.success(self.request, "Signup successful. Please login.")
        return super().form_valid(form)

class UserLogoutView(View):
    template_name = 'registration/logout.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        # Show confirmation page with popup
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if 'confirm' in request.POST:
            logout(request)
            return redirect(self.success_url)
        else:
            # Cancel pressed: redirect back or home
            referer = request.META.get('HTTP_REFERER')
            if referer and referer != request.build_absolute_uri():
                return redirect(referer)
            return redirect(self.success_url)


# class UserLogoutView(LogoutView):
#     next_page = reverse_lazy('home')



class HomeView(TemplateView):
    template_name = 'divine/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()[:8] 
    
        context['about_content'] = "Welcome to Divine Glow! We offer premium beauty services to make you shine."

        context['form'] = AppointmentForm()

        return context

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
    
class PriceView(TemplateView):
    template_name = 'divine/price.html'


class ProductListView(ListView):
    model = Product
    template_name = 'divine/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_name = self.request.GET.get('category')
        if category_name:
            return Product.objects.filter(category__name=category_name)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'divine/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_reviews = self.object.reviews.count()
        context['reviews'] = self.object.reviews.all()[:5]
        context['total_reviews'] = min(total_reviews, 20)

        return context


class SubmitReviewView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if request.user.is_authenticated:
            rating = request.POST.get('rating')
            message = request.POST.get('message')

            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                message=message
            )

        return redirect('product_detail', pk=pk)


class LoadMoreReviewsView(View):
    def get(self, request, pk):
        offset = int(request.GET.get('offset', 0))
        LIMIT = 5
        MAX_REVIEWS = 20

        total_reviews = Review.objects.filter(product_id=pk).count()

        remaining_allowed = max(0, MAX_REVIEWS - offset)
        load_count = min(LIMIT, remaining_allowed)

        reviews = Review.objects.filter(product_id=pk)\
            .order_by('-created_at')[offset:offset + load_count]

        data = []
        for review in reviews:
            data.append({
                'username': review.user.userprofile.username,
                'image': review.user.userprofile.image.url,
                'rating': review.rating,
                'message': review.message,
            })

        return JsonResponse({
            'reviews': data,
            'loaded_count': offset + len(data),
            'total_reviews': min(total_reviews, MAX_REVIEWS),
            'has_more': offset + len(data) < min(total_reviews, MAX_REVIEWS)
        })

class GalleryView(TemplateView):
    template_name = 'divine/gallery.html' 

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
            

class FeedBackCreateView(LoginRequiredMixin, CreateView):
    model = FeedBack
    form_class = FeedBackForm
    template_name = 'divine/feedback_form.html'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_success_url(self):
        return reverse_lazy('feedback-form')

    def form_valid(self, form):
        # Adding success message to the context
        messages.success(self.request, 'Thank you for your feedback!')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Adding error message to the context
        messages.error(self.request, 'All fields are required!')
        return self.render_to_response(self.get_context_data(form=form))



class NewsletterView(View):
    def get(self, request):
        return HttpResponseNotAllowed(["POST"])
        

    def post(self, request):
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return JsonResponse(
                {
                    "success": False,
                    "message": "Invalid request type.",
                },
                status=400,
            )

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

        return JsonResponse(
            {
                "success": False,
                "message": "Cannot subscribe to the newsletter.",
            },
            status=400,
        )