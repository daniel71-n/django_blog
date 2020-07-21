# pages/urls.py
from django.urls import path

from .views import HomePageView, AboutPageView, ContactPageView, SearchView

urlpatterns = [
    #path('', homePageView, name='home')
    path('', HomePageView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='searched'),
    path('about/', AboutPageView.as_view(), name='about_page'),   
    path('contact/', ContactPageView.as_view(), name='contact_page')
    ]
#note: the url must not start with a / but must end with one. --> like 'about' above
#path(route, view, **kwargs): The view argument is a view function or the result of as_view() for class-based views]
