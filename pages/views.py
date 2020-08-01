from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView
from django.db.models import Count
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.core.paginator import Paginator


from .models import Contact
from posts.models import Post,Category
from .forms import ContactForm


# Create your views here.



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


class ContactPageView(CreateView):
    model = Contact
    fields = '__all__'
    template_name='contact.html'
    #success_url = '/home/'
    success_url = reverse_lazy('home')  # redirect to the home page upon successful submission of the form

    def get_context_data(self, **kwargs):
        context = super(ContactPageView, self).get_context_data(**kwargs)
        context['form'] = ContactForm
        return context

   




def HomeAjaxView(request):
    """FBV for rendering the homepage with Ajax"""
    HOME_PAGE_TEMPLATE = 'home.html'
    AJAX_TEMPLATE = 'cards.html'    # the template that's meant to be rendered into HTML, turned into a string and sent as an Ajax response. On the client, Javascript is to replace the appropriate parts with the html contained in the response object

    def get_queryset():
       """nested function that builds the queryset that's to be paginated and sent back as a response"""
       req = request.GET.get('sort_options', None)
       if not req: # if no sort_options query string is part of the url, i.e. if a request for "" or "/home/" is made without any sorting specified, but with or without pagination
          return Post.objects.order_by('-publication_date') #then (i.e. this is made the default) - sort by most recent first
       elif req:
           if req == 'most-recent':
              return Post.objects.order_by('-publication_date')
           elif req=='least-recent':
              return Post.objects.order_by('publication_date')
           elif req=='most-comments':   #most comments first
               return Post.objects.annotate(comment_number=Count("comments")).order_by('-comment_number')
           elif req=='least-comments': 
               return Post.objects.annotate(comment_number=Count("comments")).order_by('comment_number')


    def get_page():
       """paginate the queryset built by get_queryset and return the result. Also return an is_paginated variable set to True if pagination has been done"""
       page_obj = request.GET.get('page', 1)  # if the request dict contains no 'page' key (ie no page query strig came with the http request), default to 1    
       paginator_obj = Paginator(get_queryset(), 5)  #paginate the queryset to 5 items per page
       try:
          post_list = paginator_obj.page(page_obj)   # get the page number specified in the get query querystring parameter of the URL, or the first page, by default, if no page is specified in the request
          is_paginated = True if paginator_obj.num_pages> 1 else False   #set is_Paginated to true if and only if the items span at least two pages, else False (no pagination)
       except PageNotAnInteger:
          post_list = paginator_obj.page(1)
       except EmptyPage:
          post_list = paginator_obj.page(paginator.num_pages) 
       return post_list, is_paginated


    def get_context_data():
        """build the context to be passed back to the template"""
        # Also include all the category names on the website in the context
        context = {}
        POST_LIST, IS_PAGINATED = get_page()   # call get_page to determine if there is pagination and if so get the queryset paginated

        context['categories'] = Category.objects.all()
        context['post_list'] = POST_LIST
        context['is_paginated'] = IS_PAGINATED
        context['page_obj'] = POST_LIST  #page_obj and post_list point to the same object, because post_list is actually a page object, the result of a paginated queryset

        # return any sorting query strings(i.e. sort_options="least-recent") that came attached to the url path in the request,
        # but discard any page query strings (i.e. &page=2), so that the url can be build reliably in the template
        # note that a '?' isn't prepended to the query string, so you'll have to account for that in the template too when building the url
        mutable_querydict_copy = request.GET.copy()  #By default QueryDicts are immutable, though the copy() method will always return a mutable copy.
        sort_query_string_var = mutable_querydict_copy.pop('page', True) and mutable_querydict_copy.urlencode()
        # if the queryDict contains a page query string (i.e. &page=2), drop it, and get the rest of the query strigs that came attached to the url path - get them from the dictionary and encode them as query strings
        # if there's no 'page' key in the dict (i.e. no pagination query string came with the url), then there's nothing to pop; return True so that the 'and' condition can move on and urlencode is called 
        # to encode all the dict keys (i.e. all the query string parameters other than pagination) into a query string
        # this is to be passed to the context to be used in the template by appending it to the urlpath and then appending the pagination query string to that (if pagination is used)        
      
        context['sort_query_string'] = sort_query_string_var
        return context


    CONTEXT = get_context_data()  #call the get_context_data function defined above to build up the context to be passed to render()

    if not request.is_ajax():   # check that the header contains a ('X-REQUESTED-WITH', 'XMLHttpRequest') field
       #return render(request, HOME_PAGE_TEMPLATE, {'post_list': POST_LIST, 'is_paginated': IS_PAGINATED, 'page_obj':POST_LIST })
       return render(request, HOME_PAGE_TEMPLATE, CONTEXT)

    elif request.is_ajax():
       return render(request, AJAX_TEMPLATE, CONTEXT)
       # render the partial template instead, and send the response back as an html string, which Javascript is to use in place of the part that's supposed to be replaced 




















	
