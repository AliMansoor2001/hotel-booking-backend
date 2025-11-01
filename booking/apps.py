from django.apps import AppConfig

class BookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # optional but recommended
    name = 'booking'  # must exactly match your app folder name
    verbose_name = 'Booking'


