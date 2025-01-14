from django.urls import path
from homepage import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name='homepage'),
    path('schedule/', views.schedule, name='schedule'), 
    path('services/', views.services, name='services'), 
    path('resources/', views.resources, name='resources'), 
    path('works/', views.works, name='works'), 
    path('who/', views.who, name='who'), 
    path('policy/', views.policy, name='policy'), 
    path('terms/', views.terms, name='terms'), 
    path('blog/', views.blog, name='blog'), 
    path('faq/', views.faq, name='faq'), 
    path('gallery/', views.gallery, name='gallery'), 
    path('volunteers/', views.volunteers, name='volunteers'), 
    path('register/', views.register, name='register'),
    path('login/', views.custom_login ,name='login'),
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('worker_dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact_success'),
    path('request-pickup/', views.request_pickup, name='request_pickup'),
    path('pickuphistory/', views.pickuphistory, name='pickuphistory'), 
    path('settings/', views.settings, name='settings'),
    # path('change_password/', views.change_password, name='change_password'),
 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)