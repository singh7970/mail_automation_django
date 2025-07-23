from django.contrib import admin

from .models import Subscription
# Register your models here.
from app.models import Register

admin.site.register(Register)






@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
