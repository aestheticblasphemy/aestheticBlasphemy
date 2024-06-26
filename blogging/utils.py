import os
from functools import wraps, WRAPPER_ASSIGNMENTS

from blogging.create_class import CreateClass, CreateTemplate
import re
from django.utils.functional import keep_lazy_text
import six
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import user_passes_test
import unicodedata
from django.http.response import HttpResponseForbidden

css_styles = {
			'bootstrap3': {
						'center': 'text-center',
						'left': 'text-left',
						'right': 'text-right',
						'justify': 'text-justify',
						'image': 'img-responsive',
						'gray' : 'text-muted',
						'float-left': 'pull-left',
						'float-right': 'pull-right',
						},
			'bootstrap4': {
						'center': 'text-xs-center',
						'left': 'text-xs-left',
						'right': 'text-xs-right',
						'justify': 'text-justify',
						'image': 'img-fluid',
						'gray' : 'text-muted',
						'float-left': 'pull-md-left',
						'float-right': 'pull-md-right'
						},
			'mdl': {
				},
			}

def get_css_styles():
	try:
		import django.conf.settings as settings
		if settings != None:
			return css_styles[settings.BLOGGING_CSS_FRAMEWORK]
	except ImportError:
		return css_styles['bootstrap4']


def create_content_type(name,form_dict,is_leaf):
	"""
	This function will create the form and template for new contentype
	"""
	form_filename = os.path.abspath(os.path.dirname(__file__))+"/custom/"+name.lower()+".py"
	template_filename = os.path.abspath(os.path.dirname(__file__))+"/templates/blogging/includes/"+name.lower()+".html"
	flag = False
	try:
		fd = open(form_filename, 'r')
		fd.close()
		fd1 = open(template_filename, 'r')
		fd1.close()
	except IOError:
		flag = True
	if flag:
		#We are good to go. Create the Output string that must be put in it
		create_class_object = CreateClass(name, form_dict,is_leaf)
		form_string = create_class_object.form_string()
		template_object = CreateTemplate(name, form_dict,is_leaf)
		template_string = template_object.form_string()

		try:
			fd = os.fdopen(os.open(form_filename,os.O_CREAT| os.O_RDWR , 0o555),'w')
			fd.write(form_string)
			fd.close()
			fd = os.fdopen(os.open(template_filename,os.O_CREAT| os.O_RDWR , 0o555),'w')
			fd.write(template_string)
			fd.close()

			#print((file(form_filename).read()))
			return True
		except IOError:
			print("Error Opening File for Writing")
			return False
	else:
		return False





def get_imageurl_from_data(data):

	try:
		matches = re.findall(
				r'(<img[^>].*?src\s*=\s*"([^"]+)")', str(data))
		if matches:
			return str(matches[0][1])
		else:
			return None
	except Exception as e:
		print(e)
		print("Error in get_imageurl_from_data")
		return None


def strip_image_from_data(data):
	p = re.compile(r'<img.*?/>',flags=re.DOTALL)
	line = p.sub('', data)
	#print("LOGS:: Stripping images from data")
	return line

def truncatewords(Value,limit=30):
	try:
		limit = int(limit)
		# invalid literal for int()
	except ValueError:
		# Fail silently.
		return Value

	# Make sure it's unicode
	Value = str(Value)

	# Return the string itself if length is smaller or equal to the limit
	if len(Value) <= limit:
		return Value

	# Cut the string
	Value = Value[:limit]

	# Break into words and remove the last
	words = Value.split(' ')[:-1]

	# Join the words and return
	return ' '.join(words) + '...'

@keep_lazy_text
def slugify_name(value):
	value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
	value = re.sub('[^\w\s-]', '', value).strip().lower()
	return re.sub('[-\s]+', '_', value)


def user_has_group(test_func):
    """
    Decorator for views that checks that the user has the group,
    raising HttpResponseForbidden page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=WRAPPER_ASSIGNMENTS)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return decorator


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_has_group(in_groups)

#slugify_name = allow_lazy(slugify_name, six.text_type)
