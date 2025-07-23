from django.db import models
from django.contrib.auth.models import AbstractUser
from app.managers import CustomUserManager
from django.conf import settings

class Register(AbstractUser):
    username = None  # ✅ Remove username field since using email

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    row_created_date = models.DateTimeField(auto_now_add=True)
    row_modified_date = models.DateTimeField(auto_now=True)
    row_created_by = models.CharField(max_length=50, default='sysusr')
    row_modified_by = models.CharField(max_length=50, null=True)
    has_used_trial = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No username required

    objects = CustomUserManager()  # ✅ Correct place (inside the class!)

    class Meta:
        db_table = 'register'

    def __str__(self):
        return self.email




class Subscription(models.Model):
    PLAN_CHOICES = (
        ('Monthly', 'Monthly ₹99'),
        ('Yearly', 'Yearly ₹999'),
        ('Free Trial', 'Free Trial'), 
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan}"