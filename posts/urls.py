# pages/urls.py
from django.urls import path

from .views import PostListView, PostDetailView, CategoryView

urlpatterns = [
    #path('', homePageView, name='home')
    path('', PostListView.as_view(), name='posts'),  #the as_view() method is Inherited by the PostListView class and it returns its template attribute 
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'), 
    path('cat/<str:slug>/', CategoryView.as_view(), name='in_category')
    ]


#note: the url must not start with a / but must end with one.
#path(route, view, **kwargs): The view argument is a view function or the result of as_view() for class-based views
