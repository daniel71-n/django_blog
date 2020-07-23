from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import * 


# Create your views here.


class PostListView(ListView):
    model = Post  # the model attribute is inherited from MultipleObjectMixin
    template_name = 'posts.html'  #this is another inherited attribute; this is what's returned by the .as_view() method that the class is qualified with when called in the urlconf 
    context_object_name = 'all_posts_list' # change the name of the context variable inside templates; the fault would be object_list
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        # get all the category names from the Category Model and add them to the context dictionar tied to the 'categories' key;
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
    slug_field="cat_name"  #this is necessary in order for the url matching to succeed; you need to specify the field that the slug variable (from the capturing group in the urlconf) needs to be matched against
                           #otherwise you'd get errors like "Cannot resolve keyword 'slug' into field. Choices are: cat_name, id, post"
                           #where cat_name, id, and post are obviously the existing field of the Category model














