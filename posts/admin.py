from django.contrib import admin
from .models import *
from django.forms import ModelForm

# Register your models here.

admin.site.register(Post)  # you need to register models with the admin; Post is a class declared in the models.py file. It's being registered here.

admin.site.register(Commenter)
admin.site.register(Category)
admin.site.register(Comments)

#The TextField strips whitespace, with the result that all text will have no line breaks and whatnot when displayed to the user;
#to straighten that out, the strip parameter needs to be set to False
class KeepWhitespace(ModelForm):
    def __init__(self, *args, **kwargs):
        super(KeepWhiteSpace, self).__init__(*args, **kwargs)
        self.fields['body_text'].strip = False  #make it so that text input into the body_text field keeps the whitespace intact and doesn't strip it

    class Meta:
        model = Post
        fields = "__all__"




