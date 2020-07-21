from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from posts.models import Post,Category
from django.db.models import Q



# Create your views here.

class HomePageView(ListView):
    template_name = 'home.html'
    queryset = Post.objects.order_by('-publication_date')
    context_object_name = 'post_list'    
    paginate_by = 5 #split the Post objects up into pages, 5 per page

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # Also include all the category names on the website in the context
        context['categories'] = Category.objects.all()
        return context




#template_name is a method that TemplateView inherits in turn from TemplateResponseMixin;
#The documentation says this about it: The full name of a template to use as defined by a string. Not defining a template_name will raise a django.core.exceptions.ImproperlyConfigured exception.



class SearchView(ListView):
    model = Post
    template_name = 'searched.html'
    context_object_name = 'search_results'

    def get_queryset(self):
       result = super(SearchView, self).get_queryset()
       query = self.request.GET.get('search')
       if query:
          postresult = Post.objects.filter(body_text__contains=query)
          result = postresult
       else:
           result = None
       return result


    

class AboutPageView(TemplateView):
    template_name='about.html'


class ContactPageView(TemplateView):
    template_name='contact.html'
