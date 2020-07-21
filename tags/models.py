from django.db import models

# Create your models here.


class Tags(models.Model):
    #an auto-incrementing integer primary key is added automatically unless specified otherwise, but in this particular case I'll tie the pk to the tag_name column instead 
    tag_name = models.CharField(max_length=30, primary_key=True) #a CharField with a maximum length of 30 characters; that's how long a tag can be, at most       
    def __str__(self):
        return self.tag_name #the printable representation of a Tags instance is its tag_name

    def get_absolute_url(self):
        return "/tags/{}/".format(self.tag_name)


