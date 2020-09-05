from django import forms
from django.contrib.admin import widgets
from dashboard.models import *
from taggit.models import Tag


from aestheticBlasphemy.forms import TagField

class ProfileEditForm(forms.ModelForm):
    address = forms.Textarea()
    occupation = forms.ChoiceField(choices=OCCUPATION)
    website = forms.CharField()
    date_of_birth = forms.DateField()
    interest = TagField()
    class Meta:
        model = UserProfile
        exclude = (
                   'gender',
                   'user'
                   )

