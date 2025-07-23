from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

from app.models import Subscription, Register

@login_required
def start_free_trial(request):
    user = request.user

    if user.has_used_trial:
        messages.error(request, "You have already used your free trial.")
        return redirect('index')  # or wherever you want to redirect

    # Check if subscription already exists
    subscription, created = Subscription.objects.get_or_create(user=user, defaults={
        'plan': 'Free Trial',
        'start_date': timezone.now(),
        'end_date': timezone.now() + timezone.timedelta(days=7),  # example 1st trial
        'is_active': True,
    })

    if not created:
        # Update existing subscription to be Free Trial
        subscription.plan = 'Free Trial'
        subscription.start_date = timezone.now()
        subscription.end_date = timezone.now() + timezone.timedelta(days=7)  # example duration
        subscription.is_active = True
        subscription.save()

    # Update user's trial flag
    user.has_used_trial = True
    user.save()

    messages.success(request, "Your free trial has been activated.")
    return redirect('index')
