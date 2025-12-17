from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('appointment/', views.AppointmentView.as_view(), name='appointment'),
    path('booked-slots/', views.BookedSlotsView.as_view(), name='booked_slots'),
    path("contact/", views.ContactView.as_view(), name="contact"), 
    path("newsletter/", views.NewsletterView.as_view(), name="newsletter"), 
]
