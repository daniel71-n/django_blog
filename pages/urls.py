# pages/urls.py
from django.urls import path

from .views import HomePageView, AboutPageView, ContactPageView, SearchView

urlpatterns = [
    #path('', homePageView, name='home')
    path('', HomePageView.as_view(), name='home'),
    path('home/', HomePageView.as_view(), name='home_verbose'),
    path('search/', SearchView.as_view(), name='searched'),
    path('about/', AboutPageView.as_view(), name='about_page'),
    path('contact/', ContactPageView.as_view(), name='contact_page'),
    ]
#note: the url must not start with a / but must end with one. That's becase the slash is added by default ot the bare path
#path(route, view, **kwargs): The view argument is a view function or the result of as_view() for class-based views]

#the HomePageView is used for both the bare path '' indicating the homepage, and any query strings appended to it,  as well as for '/home/' and any query strings appended to that.
#the result is that "/?sort_options=least-comments&page=2" and "/home/?sort_options=least-comments&page=2" are essentialyl the same and are both valid.



