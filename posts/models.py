from django.db import models
from django.conf import settings
from tags.models import Tags
# Create your models here.


class NonStrippingTextField(models.TextField):
    """A TextField that does not strip whitespace"""
    def formfield(self, **kwargs):
        kwargs['strip'] = False
        return super(NonStrippingTextField, self).formfield(**kwargs)


class Commenter(models.Model):
    commenter_email= models.EmailField(
            help_text="The email address is only used for computing a username, which is given by eveything before the '@' (ampersand) sign. That makes it more likely that the username will be unique withou having to think of an original username.")
    # blank=False and Null=False; the field will be required in html forms - you can't submit a comment otherwise
    def __str__(self):
        """printable name"""
        return self.commenter_email.split('@')[0]   #discard the email-provider DNS part (i.e. everything after and including '@') 
                                                    #and display everything coming before that as a username for the author of the comment






class Category(models.Model):
    cat_name = models.CharField("Category Name",   
            max_length=40,                        # the positional first argument (optional) sets an arbitrary verbose name to be displayed (e.g. on the Admin page) 
            #primary_key=True, 
            help_text="The name of a Section/Category you want to create for articles to be nested under. Useful for grouping related articles together")
   
    def __str__(self):
        """'pretty' (printable) format - e.g. the way it shows up in the admin page"""
        return self.cat_name

    def get_absolute_url(self):
              return "/posts/cat/{}/".format(self.cat_name)



class Post(models.Model):
    title = models.CharField(max_length=150)
    body_text = NonStrippingTextField()
   
    author = models.ForeignKey(settings.AUTH_USER_MODEL,   #the FK here points to the built-in user model
        on_delete=models.CASCADE)
  

    publication_date = models.DateField( # check that this is a datefield before storage in the DB 
            auto_now_add=True      # Automatically set the field to today when the object is first created.
            )

    #the section field is a foreign key to a 'section' table. Articles will then be displayed on the page under the respective cateegory title
    section = models.ForeignKey(
            'Category',
            on_delete=models.CASCADE,
            default="Etc")
            
    tags = models.ManyToManyField(Tags)
    

    def get_reading_length(self):
        """return roughly how many minutes it would take to read the article in question"""
        body_text_length= len(self.body_text.split(' ')) # split the body_text into words (using whitespace as the delimiter) and count how many words there are 
        reading_length = 'Reading time: ' + str(round(body_text_length / 200)) + ' mins'      #apparently, studies have shown that 238 words per minute is the average reading speed, but I'll round it down to 200
        #using round() to round the number to an integer, discarding any decimal digits

        return reading_length

 
    def __str__(self):     # if you don't set a str operator overloading method, the name of the post on the admin page will be post.object
        return "{}".format(self.title)


    def get_absolute_url(self):
        return "/posts/{}/".format(self.id)

    def get_comments_num(self):
        """return how many comments are associated with this post"""                                                           
        num=len(self.comments_set.all())
        return num




 
class Comments(models.Model):
    """A model storing the comments associated with a particular post."""
    comment = models.TextField(help_text="A comment to be posted under a particular post") #if the comments were allowed to be empty, blank=True would be used; They can't be empty, and the default is blank=False
    associated_post = models.ForeignKey('Post',
        on_delete = models.CASCADE,
        help_text="The respective Post that the comment is associated with. If the post is deleted, the associated comments get deleted as well.")


    author = models.ForeignKey('Commenter', 
            on_delete=models.CASCADE,
            help_text="The author of the comment. The commenter has to fill out an email address field before submitting a comment, with a username being computed from the address by discarding everything after and including the ampersand")
#--there's only one user (the writer of the blog)--; commenters don't get accounts when inputting their email when submitting a comment
# it only server to compute the username to be shown along with the comment; --> email: someuser@someemailprovider.com = username: someuser


    def __str__(self):
        """printable name"""
        return "{} : {} [...] by {}".format(self.associated_post, self.comment[:15], self.author) 
    # compute a string from the title of the associated article + the first 15 characters of the comment + [..],to indicate only part of the comment




