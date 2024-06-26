
class CreateClass():
    """ This class will generate the required class of desired content type
    and form the string that will be written to the python script file
    """
    
    def __init__(self, name, member_dict,is_leaf):
        self.import_string = 'from blogging import tag_lib\nfrom django.db import models\nfrom blogging.models import *\nfrom django import forms\n' + \
        'from blogging.forms import *\nfrom django_ckeditor_5.widgets import CKEditor5Widget\nimport json\n' + \
        'from django.db.models import Q \nfrom mptt.forms import TreeNodeChoiceField\nfrom crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit\n' 
        self.file_start = '"""\nThis is auto generated script file.\nIt defined the wrapper class for specified content type.\n"""\n'
        self.class_name = 'class ' + str(name).capitalize() +'Form(forms.Form):\n'

        # List to store the member of the Class
        self.class_member_string_list = [ ]
        # add the title, section and tag fields
        self.class_member_string_list.append('\ttitle = forms.CharField(max_length = 100)\n')
        self.class_member_string_list.append('\tpid_count = forms.IntegerField(required=False)\n')
        if is_leaf == True:
            self.class_member_string_list.append('\tsection = TreeNodeChoiceField(queryset=BlogParent.objects.all().filter(~Q(title="Orphan"),Q(children=None)),required=True,empty_label=None, label = "Select Section" )\n')
            
        else:
            self.class_member_string_list.append('\tparent = TreeNodeChoiceField(queryset=BlogParent.objects.all().filter(~Q(title="Orphan"),~Q(title="Blog")),required=True,empty_label=None, label = "Select Parent" )\n')
        
        # string for init function
        self.class_initfunction_string = '\tdef __init__(self,action, *args, **kwargs):\n'
        self.class_initfunction_string += '\t\tself.helper = FormHelper()\n\t\tself.helper.form_id = "id-'+ str(name).capitalize() +'"\n\t\tself.helper.form_class = "form-horizontal"\n'
        self.class_initfunction_string += '\t\tself.helper.label_class = "col-lg-2"\n\t\tself.helper.field_class = "col-lg-8"\n\t\tself.helper.form_method = "post"\n'
        self.class_initfunction_string += '\t\tself.helper.form_action = action\n'
        self.class_initfunction_string += '\t\tself.helper.layout = Layout(\n\t\t\tFieldset(\n\t\t\t"Create The Content of Type ' + str(name).capitalize() + ' ",\n'
        self.class_initfunction_string += '\t\t\t"title",\n'


        #string for save function
        self.class_formclass_save_string = '\tdef save(self,post,commit=False):\n' + '\t\tpost.pop("csrfmiddlewaretoken")\n\t\tpost.pop("submit")\n' 
        self.class_formclass_save_string += '\t\tpost.pop("title")\n' 
        if is_leaf == True:
            self.class_formclass_save_string += '\t\tpost.pop("section")\n'
            self.class_formclass_save_string += '\t\tpost.pop("tags")\n'
        else:
            self.class_formclass_save_string += '\t\tpost.pop("parent")\n'
        
        # commit False case
        self.class_formclass_save_string += '\t\tif commit == False:\n'
        self.class_formclass_save_string += '\t\t\tfor k,v in post.iteritems():\n\t\t\t\tif str(k) == "pid_count" :\n\t\t\t\t\tpost["pid_count"] = self.cleaned_data["pid_count"]\n'
        self.class_formclass_save_string += '\t\t\t\telse:\n\t\t\t\t\tpost[k] = str(v.encode("utf-8"))\n'
        self.class_formclass_save_string += '\t\t\treturn json.dumps(post.dict())\n'
        
        # commit True Test
        self.class_formclass_save_string += '\t\tfor k,v in post.iteritems():\n\t\t\tif str(k) != "pid_count" :\n\t\t\t\ttmp = {}\n'
        self.class_formclass_save_string += '\t\t\t\ttmp = tag_lib.insert_tag_id(str(v.encode("utf-8")), self.cleaned_data["pid_count"])\n'
        self.class_formclass_save_string += '\t\t\t\tpost[k] = tmp["content"]\n'
        self.class_formclass_save_string += '\t\t\t\tpost["pid_count"] = tmp["pid_count"]\n'
        self.class_formclass_save_string += '\t\treturn json.dumps(post.dict())\n'
        
        
       
        for member_name, member_type in list(member_dict.items()):
                 
            ## Creating form fields in FormClass
            if str(member_type) == 'TextField':
                class_member = '\t' + member_name + ' = forms.CharField(widget = CKEditor5Widget(config_name="author",attrs={"class": "django_ckeditor_5"}), required=False)\n'
            if str(member_type) == 'CharField':
                class_member = '\t' + member_name + ' = forms.CharField(max_length=100, required=False)\n'
            self.class_member_string_list.append(class_member)

            self.class_initfunction_string += '\t\t\t"' + member_name + '",\n'

        # add the tags in member list
        if is_leaf == True:
            self.class_initfunction_string += '\t\t\t"section",\n'
        else:
            self.class_initfunction_string += '\t\t\t"parent",\n'
        self.class_initfunction_string += '\t\t\tField("pid_count", type="hidden"),\n'
        if is_leaf == True:
            self.class_member_string_list.append('\ttags = TagField()\n')
            self.class_initfunction_string += '\n\t\t\t"tags",\n'

        # add button etc.
        self.class_initfunction_string += '\t\t\t ),\n\t\t\tButtonHolder(\n\t\t\tSubmit("submit", "Publish", css_class="button blue"),\n\t\t\t\tSubmit("submit", "Save Draft", css_class="button white")\t\t\t),\n\t\t)\n'
        self.class_initfunction_string += '\t\tsuper(' + str(name).capitalize() +'Form' + ', self).__init__(*args, **kwargs)\n\n\n\n'


    
    def form_string(self):
        
        final_string =  self.import_string + self.file_start + self.class_name
        for member in self.class_member_string_list:
            #print final_string
            final_string += member

        final_string += self.class_initfunction_string + self.class_formclass_save_string
        
        return final_string
    

class CreateTemplate():
    """
    This class will auto generate the template to be used for Detail page of that content type object
    """
    def __init__(self, name, member_dict,is_leaf):
        self.start_string = '{% extends "blogging/test_detail.html" %}\n'
        self.start_string += '\t{% block custom_detail %}\n'
        self.start_string += '\t\t{% autoescape off %}\n'
        self.member_list = []
        self.end_string = '\t\t{% endautoescape %}\n\t{% endblock %}\n'
        for member_name, member_type in list(member_dict.items()):
            member_string = '\n\t\t\t{{ content.' + member_name + ' }}\n'
            self.member_list.append(member_string)
    
    def form_string(self):
        final_string = self.start_string 
        for member in self.member_list:
            final_string += member
        final_string += self.end_string
        return final_string 
          


def test_fun():
    name = 'basecontent'
    member_dict = {'title': 'TextField',
                   'content': 'TextArea',
                   'Author' : 'TextField'
                   }
    
    create_class = CreateClass(name,member_dict)
    
    string =  create_class.form_string()
    print(string)
