from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import * 

class PostListView(ListView):
    model = Post  # the model attribute is inherited from MultipleObjectMixin
    template_name = 'posts.html'  #this is another inherited attribute; this is what's returned by the .as_view() method that the class is called with
    context_object_name = 'all_posts_list' #this is used in Django template language for loops; if you didn't set the name it would be object_list
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        # get all the category names from the Category Model and add them to the context dictionary;
        context['categories'] = Category.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post' #if we don't override this, the default would have to be used, which is object, e.g. {{ object.title }}



class CategoryView(DetailView):
    model = Category
    template_name = 'cats.html'
    context_object_name = 'cat' 
    slug_field="cat_name"  #this is necessary in order for the url matching to succeed; you need to specify the field that the slug variable (from the capturing group) needs to be matched against
                           #otherwise you'd get errors like "Cannot resolve keyword 'slug' into field. Choices are: cat_name, id, post"

