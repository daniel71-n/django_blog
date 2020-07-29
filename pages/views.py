from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from posts.models import Post,Category
from django.db.models import Count

# Create your views here.




class HomePageView(ListView):
    template_name = 'home.html'
    #queryset = Post.objects.order_by('-publication_date')
    model=Post  #if not defined (and queryset is not defined (above) either) but get_queryset is, you'll (still) get an 
    #error like django.core.exceptions.ImproperlyConfigured: HomePageView is missing a QuerySet. Define HomePageView.model, HomePageView.queryset, or override HomePageView.get_queryset().

    def get_queryset(self):   #construct the queryset based on the sorting query string (if present) in the http request or lack thereof (use the default)
       result = super(HomePageView, self).get_queryset()
       req = self.request.GET.get('sort_options', None)   #get the sort_options parameter from the URL, if present, else None(i.e. no sort_options query came with the url)
       if not req: # if no sort_options query string is part of the url, i.e. if a request for "" or "/home/" is made without any sorting query appended to it
           return Post.objects.order_by('-publication_date') #then (i.e. this is made the default) - sort by most recent first
       elif req:    # if the url DOES come with a query string accessible with the sort_options parameter, then check to see what sorting options has been selected and construct the queryset based on that
           if req == 'most-recent':  
              return Post.objects.order_by('-publication_date')  # this is the default, but it's made so that it can also be requested explictly (e.g. if re-selecting it after having selected a different option)
           elif req=='least-recent':
              return Post.objects.order_by('publication_date')
           elif req=='most-comments':   # sort by most comments first
               return Post.objects.annotate(comment_number=Count("comments")).order_by('-comment_number')        
           elif req=='least-comments':
               return Post.objects.annotate(comment_number=Count("comments")).order_by('comment_number')

    context_object_name = 'post_list'   
    paginate_by = 5 #split the Post objects up into pages, 5 per page

    def get_context_data(self, **kwargs): # build the context to be passed to the template; a few variables need to be attached: crucially, the sorting query string, if any; read "multiple query strings and pagination" below
        context = super(HomePageView, self).get_context_data(**kwargs)
        # Also include all the category names on the website in the context
        context['categories'] = Category.objects.all()
        
    # return any sorting query strings(i.e. sort_options="least-recent") that came attached to the url path in the request,
    # but discard any page query strings (i.e. &page=2), so that the url can be build reliably in the template
    # note that a '?' isn't prepended to the query string, so you'll have to account for that in the template too when building the url
        mutable_querydict_copy = self.request.GET.copy()   # By default QueryDicts are immutable, though the copy() method will always return a mutable copy.
        sort_query_string_var = mutable_querydict_copy.pop('page', True) and mutable_querydict_copy.urlencode()
        # if the queryDict contains a page query string (i.e. &page=2), drop it, and get the rest of the query strigs that came attached to the url path - get them from the dictionary and encode them as query strings
        # if there's no 'page' key in the dict (i.e. no pagination query string came with the url), then there's nothing to pop; return True so that the 'and' condition can move on and urlencode is called 
        # to encode all the dict keys (i.e. all the query string parameters other than pagination) into a query string
        # this is to be passed to the context to be used in the template by appending it to the urlpath and then appending the pagination query string to that (if pagination is used)
        context['sort_query_string'] = sort_query_string_var

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
