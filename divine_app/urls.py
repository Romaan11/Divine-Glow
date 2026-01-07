from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServiceView.as_view(), name='services'),
    path('price/', views.PriceView.as_view(), name='price'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/review/', views.SubmitReviewView.as_view(), name='submit_review'),
    path('product/<int:pk>/reviews/', views.LoadMoreReviewsView.as_view(), name='load_more_reviews'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('appointment/', views.AppointmentView.as_view(), name='appointment'),
    path('booked-slots/', views.BookedSlotsView.as_view(), name='booked_slots'),
    path("contact/", views.ContactView.as_view(), name="contact"), 
    path('feedback/', views.FeedBackCreateView.as_view(), name='feedback-form'),
    path("newsletter/", views.NewsletterView.as_view(), name="newsletter"), 

    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    # path('choose-otp/', views.OTPChoiceView.as_view(), name='choose_otp'),
    path('verify-otp/', views.OTPVerifiyView.as_view(), name='verify_otp'),
]