from django.db import models
from divine_app.validators import max_20_words


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

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
    
class Newsletter(TimeStampModel):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email