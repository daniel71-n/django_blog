from django.db import models
from pages.models import Contact

from django.forms import ModelForm


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        #fields = ['sender_name', 'sender_email', 'additional_contact_information', 'about', 'inquiry_details']
        fields = '__all__'   # display all fields in the template form generated

        labels = {'sender_name': 'Your name ',
                  'sender_email' : 'Your email address ',
                  'additional_contact_information': 'Additional contact information (optional)  ',
		  'inquiry_details': 'Inquiry details (optional) '
                }

        help_texts = {'sender_name': '',
                'about':"a summary of what it is you're trying to reach out about",
                'sender_email': '',
                 'sender_email': '',
                  'additional_contact_information' : 'Optional extra contact details, such as a phone number you can be reached at, an alternative email address etc.'
                 }


        def clean_due_back(self):
            #data_to_validate = self.cleaned_data['data_to_validate']
            #take action to validate data_to_valodate

            #return data
            pass


