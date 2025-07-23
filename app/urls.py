from django.urls import path
from app.views import index  
from . import views
from .views.login_page import  login_page
from .views.register_page import  register_page
from .views.subscription import subscription_page
from .views.logout_page import logout_view
from .views.free_trial import start_free_trial
from .views.ai_genrativ import ai_generate_view




urlpatterns = [
    path('start-free-trial/', start_free_trial, name='start_free_trial'),
    path("register/",register_page,name="register_page"),
    path("api/ai-generate/", ai_generate_view, name="ai_generate"),
    path("",login_page,name="login_page"),
    path('index/', index, name='index'),
    path('api/fetch-emails/', views.fetch_emails_api, name='fetch_emails_api'),
    path('logout/', logout_view, name='logout_view'),
    path('subscription/', subscription_page, name='subscription'),

]

