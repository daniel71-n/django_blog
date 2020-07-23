from django.shortcuts import render

# Create your views here

from django.views.generic import TemplateView,DetailView
from .models import *

class TagsView(DetailView):
    model = Tags  
    template_name = 'tags.html'  
    context_object_name = 'tag'




