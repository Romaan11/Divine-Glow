from django.db import models

# Create your models here.
class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Appointment(TimeStampModel):
    SERVICE_CHOICES = [
        ('Hair Cut', 'Hair Cut'),
        ('Facial', 'Facial'),
        ('Massage', 'Massage'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    service = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES
    )
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
        return f"{self.name} - {self.preferred_date}"

class Contact(TimeStampModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name
    
class Newsletter(TimeStampModel):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email