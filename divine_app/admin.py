from django.contrib import admin
import divine_app.models as models

admin.site.register(models.UserProfile)
admin.site.register(models.Service)
admin.site.register(models.Appointment)
admin.site.register(models.Contact)
admin.site.register(models.FeedBack)
admin.site.register(models.Newsletter)
