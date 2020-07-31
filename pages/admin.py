from django.contrib import admin

# Register your models here


from pages.models import Contact



class ContactAdmin(admin.ModelAdmin):
    #fields= ['sender_name', 'about'] #specify the fields to be displayed; all will be displayed by default

    readonly_fields= ['submission_date']   #by default fields where auto_now_add is set to true (and thus 'editable' is set to false) won't show up in the admin
                                           # to change that, an Admin class needs to be set up and the readonly_fields parameter overridden
    class Meta:
        model= Contact


admin.site.register(Contact, ContactAdmin)   
#register the Contact model with the Admin, while specifying the Admin class to be used: ContactAdmin here, where the readonly_fields parameter's value is overridden




                                                                                                                                                                                                               
           
