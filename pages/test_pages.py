from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Category, Post



#methods need to start with "test*" to run, e.g. test_about_page_get_status_code
# some_method() won't work as the name is wrong

#the paths need to both start and end with a '/', otherwise you'll get a 404
#response = self.client.get('/about/') - thil will work but
#('about/') won't and neither will ('/about')



class HomePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(cat_name="Random")  # this is necessary as it's required in the 'section' foreign key field, so it has to be set up first
        User.objects.create(username="someuser", password="somepassword")
               
        #set up n>paginate_by post objects to check that pagination works
        for i in range(1,8):   # pagination is for 5 items per page; set up 7 Post objects
            Post.objects.create(title="Post_no{}".format(i), body_text="this is some text", author=User.objects.get(id=1), section=Category.objects.get(id=1))
        #The testing here isn't for the 'Post' model; I'll set tests for that in the corresponding package directory; here I'm only setting some Post objects up to test pagination on the home page
    
    def test_home_page_get_200_status_code(self):  # see if the client gets a 200 HTTP response code, meaning success. 
        response = self.client.get('/')  # the bare url pointing to the homepage
        self.assertEqual(response.status_code, 200)

    def test_homepage_reverse_url_by_name(self):
        response = self.client.get(reverse('home'))   # 'home' is the name argument passed in the urlconf file based on which the url can be reconstructed. Test if it works as it should
        self.assertEqual(response.status_code, 200)

    def test_homepage_correct_template_used(self):    # check to see if the home.html template is used as expected
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_pagination_homepage_is_paginated_by_5(self):
        # I set up 7 post objects (range(1,8); the view paginates by 5 pages;
        # so there should be 2 pages - 5 posts on the first page, 2 on the second
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated']==True)
        self.assertTrue(len(response.context['post_list'])==5)  # post_list is the context_object_name in the views file of the pages app
        

    def test_homepage_pagination_two_posts_left_on_the_second_page(self):   # check that 2/7 posts are indeed left over on page 2
        response = self.client.get(reverse('home')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.context['post_list']), 2)


        

class SearchPageView_tests(TestCase):
    """tests to verify that the search function works"""
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(cat_name="Somecategory")
        # this is necessary as it's required in the section foreign key field, so it has to be set up first
        User.objects.create(username="someuser", password="somepassword")
        # same as above. Posts require an author field, which can't be null
        
        Post.objects.create(title="SomePost", body_text="this is some text", author=User.objects.get(id=1), section=Category.objects.get(id=1))
        #setting a post object so that we can use the search function on a string from its text_body field
               
    def test_search_page_get_200_status_code(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_search_page_query_successful_string_found(self):
        query_text = "".join('+' + i for i in "some text".split(' '))  # 'some text' is part of the body_text field we defined above
        response = self.client.get(reverse('searched') + '?search=' + query_text)
        # the search url is supposed to look like '/search/?search=+some+text
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['search_results']), 1)  # if the search found any results - as it should, because the string used does exist - the length above should be 1. If it's 0, the search query failed




class AboutPageView_tests(SimpleTestCase):
    def test_AboutPage_get_200_status_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_AboutPage_correct_template_used(self):
        response = self.client.get(reverse('about_page'))
        self.assertTemplateUsed(response, 'about.html')


    def test_AboutPage_reverse_url_by_name(self):
        response = self.client.get(reverse('about_page'))
        self.assertEqual(response.status_code, 200)



class ContactPageView_tests(SimpleTestCase):
    def test_ContactPage_get_200_status_code(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        
    def test_ContactPage_correct_template_used(self):
        response = self.client.get(reverse('contact_page'))
        self.assertTemplateUsed(response, 'contact.html')

        
    def test_ContactPage_reverse_url_by_name(self):
        response = self.client.get(reverse('contact_page'))
        self.assertEqual(response.status_code, 200)

        
