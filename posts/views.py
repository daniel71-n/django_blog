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
    template_name='post_detail.html'
    model = Post
    context_object_name = 'post' 
    
    def get_context_data(self, **kwargs):
        context=super(PostDetailView, self).get_context_data(**kwargs)
        
        all_articles = [i.title for i in self.object.section.post_set.all()]  # make the queryset into a list, so that it can be indexed
        current_index = all_articles.index(self.object.title)     # querysets aren't lists, but can be converted to one

        # determine whether or not there's a previous article
        if current_index > 0:   # there's at least one article before this
            previous_neighbor_title = all_articles[current_index-1]    # get the title at the index before current_index
            prev_obj = Post.objects.get(title=previous_neighbor_title)   # get the object that has that title
            context['previous'] = prev_obj    # make this object accessible via a 'previous' context variable
        else:
            context['previous'] = False   # there's no 'previous' article, which needs to be reflected on the Web page
      
       # determine whether or not there's a next article
        if len(all_articles) >= current_index+2:     # if there's at least one more article in this category after this one
            next_neighbor_title = all_articles[current_index+1] 
            next_obj = Post.objects.get(title=next_neighbor_title)
            context['next'] = next_obj 
        else:
            context['next'] = False

        return context


class CategoryView(DetailView):
    model = Category
    template_name = 'cats.html'
    context_object_name = 'cat' 
    slug_field="cat_name"  #this is necessary in order for the url matching to succeed; you need to specify the field that the slug variable (from the capturing group in the urlconf) needs to be matched against
                           #otherwise you'd get errors like "Cannot resolve keyword 'slug' into field. Choices are: cat_name, id, post"
                           #where cat_name, id, and post are obviously the existing field of the Category model














