from django.db import models

# Create your models here.


class Contact(models.Model):
    sender_name = models.CharField(max_length=50)
    sender_email= models.EmailField(
            help_text="The email address of the individual who made contact")

    additional_contact_information = models.TextField(blank=True)
    #should be optional; the person using the contact form can write here a phone number, address, whatever, so that they can be more easily or conveniently reached 

    about = models.CharField(max_length=150,
                            help_text="A summary of what the inquiry is about")
    inquiry_details = models.TextField(help_text="A more detailed description of the inquiry", blank=True)

    submission_date = models.DateField(auto_now_add=True)   # automatically set the date when the entry is added to the databse

    def __str__(self):
        """printable name"""
        return "%s : %s" % (self.sender_name, self.about[:50])
