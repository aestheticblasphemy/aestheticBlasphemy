from django import forms

from django.conf import settings

from django.contrib.admin import widgets
from blogging.models import *

import taggit
from blogging.widgets import SelectWithPopUp
from django.db import models
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit

import json
from blogging import tag_lib
from blogging.utils import slugify_name

from aestheticBlasphemy.forms import TagField

CUSTOM_FIELD_TYPE = (
	('CharField', 'TextField'),
	('TextField', 'TextArea'),
#	('ImageField', 'Image'),
#	('FileField', 'File Upload'),
#	('IntegerField', 'Number'),
)

CONTACT_TYPE = (
			('Queries','Make a Query!'),
			('FeedBack','Give Your Feedback!'),
			('Feature','Suggest A Feature!'),
			('Join','Join Us!'),
			)

def validate_empty(value):
	if value :
		raise ValidationError(u'It seems you are not human!!!')

class ContentTypeForm(forms.Form):
	ContentType = forms.ModelChoiceField(
					queryset=BlogContentType.objects.all(),
					empty_label=None,
					required = True,
					label = "Select Content type or Create New!",
					widget=SelectWithPopUp)
	def __init__(self, *args, **kwargs):
		super(ContentTypeForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		
		self.helper.form_id = 'id-ContentTypeForm'
#		self.helper.form_class = 'blueForms'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-8'
		self.helper.form_method = 'post'
#		self.helper.form_action = reverse('blogging:contact-us')
		self.helper.layout = Layout(
				Fieldset(
                'You can select the existing Content Type or Create New for your Post.',
                'ContentType',
            ),
			
            ButtonHolder(
                Submit('submit', 'next', css_class='button white'),
                Submit('submit', 'delete', css_class='btn-danger')
                
            ),
			
			)


class ContentTypeCreationForm(forms.ModelForm):

	helper1 = FormHelper()
	
	def __init__(self, *args, **kwargs):
		
		super(ContentTypeCreationForm, self).__init__(*args, **kwargs)
		
		self.helper1.form_id = 'id-ContentTypeCreationForm'
		#		self.helper.form_class = 'blueForms'
		self.helper1.form_class = 'form-inline'
		self.helper1.field_template = 'bootstrap3/layout/inline_field.html'
		self.helper1.form_tag = False
#		self.helper1.template = 'blogging/inline_field.html'


	
	class Meta:
		model = BlogContentType
		fields = ['content_type', 'is_leaf',]

class FieldTypeForm(forms.Form):
	field_name = forms.CharField()
	field_type = forms.ChoiceField(widget = forms.Select(),choices=CUSTOM_FIELD_TYPE)
	
	def clean_field_name(self):
		print "LOGS: clean_field_name called"
		data = slugify_name(self.cleaned_data['field_name'])
		return data

	
class FormsetHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super(FormsetHelper, self).__init__(*args, **kwargs)
		
		self.form_id = 'id-FieldTypeForm'
#		self.helper.form_class = 'blueForms'
		self.form_class = 'form-inline'
		self.field_template = 'blogging/inline_field.html'
		self.form_method = 'post'
		self.form_tag = False
#		self.template = 'blogging/table_inline_formset.html'
		self.layout = Layout(
                'field_name',
                'field_type',
			)
	
class ContactForm(forms.Form):
	contact_type = forms.ChoiceField(label="Choose Type of Contact",required=True,
									widget = forms.Select(),choices=CONTACT_TYPE)
	name = forms.CharField(
        label="What is your name?",
        max_length=80,
        required=True,
    )
	
	email = forms.EmailField(
			label="Your email?",
			required=True,
							)
	content = forms.CharField(widget=forms.Textarea,
				label="Want to say something?",
				required=True,
				)
	extra = forms.CharField(
						label="Leave it blank if you are Human",
						validators=[validate_empty],
						required=False)
	honeypot = forms.CharField(
							label="Not visible to you",
							required=False,
							validators=[validate_empty],
							)
	
	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		
		self.helper.form_id = 'id-ContactForm'
#		self.helper.form_class = 'blueForms'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-8'
		self.helper.form_method = 'post'
#		self.helper.form_action = reverse('blogging:contact-us')
		self.helper.layout = Layout(
				Fieldset(
                'Queries, Questions, Suggestions, Feedback or for giving a pat on our back, please feel free to contact Us',
                'contact_type',
                'name',
                'email',
                'content',
                'extra',
				Field('honeypot', type="hidden"),
            ),
			
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            ),
			
			)
#		self.helper.add_input(Submit('submit', 'Submit'))

class TestFormClass(forms.Form):
	title = forms.CharField(max_length = 100)
	description = forms.CharField(widget=forms.Textarea, required=False)
	note = forms.CharField(widget=forms.Textarea, required=False)
	tags = TagField()
	section = forms.ModelChoiceField(queryset= BlogParent.objects.filter(children=None) , empty_label=None)
	pid_count = forms.IntegerField(required=False)
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		
		self.helper.form_id = 'id-TestFormClass'
#		self.helper.form_class = 'blueForms'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-8'
		self.helper.form_method = 'post'
		self.helper.form_action = reverse('blogging:testing-view')
		self.helper.layout = Layout(
				Fieldset(
                'Testing the JSON FORM',
                'title',
                'description',
                'note',
                'tags',
                'section',
                Field('pid_count', type="hidden"),
            ),
			
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            ),
			
			)
		super(TestFormClass, self).__init__(*args, **kwargs)

	
	def save(self,post,db_instance=None):
		print "LOGS: Section --> ", post.pop('section')
		print "LOGS: Tags --> ", post.pop('tags')
		print "LOGS: Tags --> ", post.pop('title')
		post.pop('csrfmiddlewaretoken')
		post.pop('submit')
		if db_instance != None:
			instance = db_instance
		else:
			instance = BlogContent()
		instance.title = self.cleaned_data["title"]
		instance.section = self.cleaned_data["section"]

		for k,v in post.iteritems():
			if str(k) != 'pid_count' :
				tmp = {}
				tmp = tag_lib.insert_tag_id(str(v),self.cleaned_data["pid_count"])
				post[k] = tmp['content']
				post['pid_count'] = tmp['pid_count']
			
		json_str = json.dumps(post.dict())
		instance.data = str(json_str)
		print "LOGS: printing the json_str", json_str
		return instance
		

"""
class PageForm(forms.Form):
        title = forms.CharField()
	parent = forms.ModelChoiceField(queryset= BlogParent.objects.filter(children=None) , empty_label=None)
	content_type = forms.ModelChoiceField(queryset = BlogContentType.objects.all(),empty_label=None)
        body = forms.CharField( widget=TextEditorWidget(attrs = {'toolbar': 'HTMLField'}) )

        def clean_title(self):
                title = self.cleaned_data['title']
                num_words = len(title.split())
                if num_words < 4:
                    raise forms.ValidationError("Not enough words!")
                return title

        def clean_body(self):
                body = self.cleaned_data['body']
                num_words = len(body.split())
                if num_words < 4:
                    raise forms.ValidationError("Not enough words!")
                return body


"""
