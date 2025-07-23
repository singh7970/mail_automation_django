from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Subscription

@login_required(login_url='/')
def subscription_page(request):
    if request.method == 'POST':
        plan = request.POST.get('plan')
        action = request.POST.get('action')

        if action == 'skip':
            # Redirect to index without activating services
            return redirect('index')

        if plan in ['monthly', 'yearly']:
            sub, created = Subscription.objects.get_or_create(user=request.user)
            sub.plan_type = plan
            sub.is_active = True
            sub.save()
            return redirect('index')

    return render(request, 'subscription.html')
