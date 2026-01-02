from django.db import models
from divine_app.validators import max_20_words
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=10, unique=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Automatically create a profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, username=instance.username, email=instance.email, phone='') 

# Automatically delete profile when user is deleted
@receiver(post_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.delete()


class Service(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='services/%Y/%m/%d',null=True, blank=True)
    description = models.TextField(
        validators=[max_20_words],
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name        

class Appointment(TimeStampModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['preferred_date', 'preferred_time'],
                name='unique_appointment_slot'
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.preferred_date} - {self.service.name}"

class Contact(TimeStampModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name
    
class FeedBack(TimeStampModel):
    RATING_CHOICES = [(i, str(i)) for i in range(1,6)]
    name = models.CharField(max_length= 100)
    image = models.ImageField(upload_to='feedback/%Y/%m/%d',null=True, blank=True)
    message = models.TextField()
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
        help_text="Rate from 1 to 5"
    )

    def __str__(self):
        return f"{self.name} - {self.rating} stars"
    
class Newsletter(TimeStampModel):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email