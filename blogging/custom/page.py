from blogging import tag_lib
from django.db import models
from blogging.models import *
from django import forms
from blogging.forms import *
#from ckeditor.widgets import CKEditorWidget
from django_ckeditor_5.widgets import CKEditor5Widget
import json
from django.db.models import Q 
from mptt.forms import TreeNodeChoiceField
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit
"""
This is auto generated script file.
It defined the wrapper class for specified content type.
"""
class PageForm(forms.Form):
	title = forms.CharField(max_length = 100)
	pid_count = forms.IntegerField(required=False)
	section = TreeNodeChoiceField(queryset=BlogParent.objects.all().filter(~Q(title="Orphan"),Q(children=None)),required=True,empty_label=None, label = "Select Section" )
	body = forms.CharField(widget = CKEditor5Widget(config_name='author',
                                                    attrs={"class": "django_ckeditor_5"}), required=False)
	tags = TagField()
	def __init__(self,action, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_id = "id-Page"
		self.helper.form_class = "form-horizontal"
		self.helper.label_class = "col-lg-2"
		self.helper.field_class = "col-lg-8"
		self.helper.form_method = "post"
		self.helper.form_action = action
		self.helper.layout = Layout(
			Fieldset(
			"Create The Content of Type Page ",
			"title",
			"body",
			"section",
			Field("pid_count", type="hidden"),

			"tags",
			 ),
			ButtonHolder(
			Submit("submit", "Publish", css_class="button blue"),
				Submit("submit", "Save Draft", css_class="button white")			),
		)
		super(PageForm, self).__init__(*args, **kwargs)



	def save(self,post,commit=False):
		post.pop("csrfmiddlewaretoken")
		post.pop("submit")
		post.pop("title")
		post.pop("section")
		post.pop("tags")
		if commit == False:
			for k,v in post.items():
				if str(k) == "pid_count" :
					post["pid_count"] = self.cleaned_data["pid_count"]
				else:
					post[k] = str(v.encode("utf-8"))
			return json.dumps(post.dict())
		for k,v in post.items():
			if str(k) != "pid_count" :
				tmp = {}
				tmp = tag_lib.insert_tag_id(str(v.encode("utf-8")), self.cleaned_data["pid_count"])
				post[k] = tmp["content"]
				post["pid_count"] = tmp["pid_count"]
		return json.dumps(post.dict())
