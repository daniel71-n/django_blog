from django.shortcuts import render

# Create your views here

from django.views.generic import TemplateView,DetailView
from .models import *

class TagsView(DetailView):
    model = Tags  
    template_name = 'tags.html'  
    context_object_name = 'tag'

    #def get_context_data(self, **kwargs):
     #   context = super(PostListView, self).get_context_data(**kwargs)
        # get all the category names from the Category Model and add them to the context dictionary;
      #  context['categories'] = Category.objects.all()
#        return context


