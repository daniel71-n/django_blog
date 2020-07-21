# pages/urls.py
from django.urls import path

from .views import TagsView

urlpatterns = [
    #path('', homePageView, name='home')
    path('<pk>/', TagsView.as_view(), name='tagged_posts') 
]


#note: the url must not start with a / but must end with one. --> like 'about' above
#path(route, view, **kwargs): The view argument is a view function or the result of as_view() for class-based views]
