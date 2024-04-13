"""@package PirateDocs
	This is main view module for Blogging app supporting various view provided to the User.
"""

import sys

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404 , HttpResponseBadRequest, JsonResponse
from blogging.models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blogging.forms import *
from django.forms.formsets import formset_factory
from django.utils.html import escape
from blogging.utils import *
from blogging.wrapper import *
import os, errno
from django.db.models import Q
from django.core.mail import mail_admins
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
use_reversion = getattr(settings, 'BLOGGING_USE_REVERSION', False)
if use_reversion:
	import reversion

# from reversion.helpers import generate_diffs
from django.contrib.contenttypes.models import ContentType

from meta_tags.views import Meta
from blogging.utils import slugify_name
from django.utils.html import strip_tags

import traceback
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

import datetime

from events.signals import generate_event
from django.utils import timezone

@login_required
@group_required('Administrator','Author','Editor')
def content_type(request):
	"""
	This view asks the user to choose content type from the existing one or
	create new content type to fit for his/her needs to create posts.

	Operations:
	NEXT -- Go to next page for creation of New content based on selected
			content type.
	DELETE -- Delete the current selected content type
			(requires admin authorizations )
	NEW -- Create New content type.
	"""

	if request.method == "POST":
		form = ContentTypeForm(request.POST)
		if form.is_valid():
			action = request.POST.get('submit')
			content_info = form.cleaned_data['ContentType']

			if action == 'next':
				#print((content_info, type(content_info)))
				request.session['content_info_id'] = content_info.id
				return HttpResponseRedirect(
		            reverse("blogging:create-post"))
			elif action == 'delete':
				if not request.user.is_staff:
					# return permission denied
					return HttpResponse(status=403)
				try:
					filename = os.path.abspath(os.path.dirname(__file__))+"/custom/"+content_info.__str__().lower()+".py"
					os.remove(filename)
					filename = os.path.abspath(os.path.dirname(__file__))+"/templates/blogging/includes/"+content_info.__str__().lower()+".html"
					os.remove(filename)
					content_info.delete()
				except OSError as e: # this would be "except OSError, e:" before Python 2.6
					raise # re-raise exception if a different error occured
			else:
				return HttpResponseBadRequest()

	else:

		if bool(request.user.groups.filter(name__in=['Author','Editor'])):
			request.session['content_info_id'] = 5
			# for this type of User we want them to create just
			# article so set the content type accordingly
			try:
				content_info_obj = BlogContentType.objects.get(
	                content_type="article"
	            )
				request.session['content_info_id'] = content_info_obj.id
				return HttpResponseRedirect(
		            reverse("blogging:create-post"))
			except ObjectDoesNotExist:
				del request.session['content_info_id']
				form = ContentTypeForm()
		if 'content_info_id' in request.session:
			try:
				content_info_obj = BlogContentType.objects.get(
	                id=request.session['content_info_id']
	            )
				data = { 'ContentType':content_info_obj	}
				form = ContentTypeForm(initial=data)
			except ObjectDoesNotExist:
				del request.session['content_info_id']
				form = ContentTypeForm()
		else:
			form = ContentTypeForm()
	return render(request,
	    "blogging/content_type.html",
	    locals())

@login_required
@group_required('Administrator','Editor','Author')
def new_post(request):
	"""
	Used for creating new post depending upon the content type chosen by the
	user in previous step.
	If content type is not selected then redirect to content-type page for
	selection of appropriate content type.

	Operations:
	BACK -- Go back to previous step for selecting new content type.
	SAVE -- Save the content as draft for later revision. todo:

	SUBMIT -- Submit the post for moderation and publication.
	"""
	if 'content_info_id' not in request.session:
		return HttpResponseRedirect(reverse("blogging:content-type"))

	content_info_obj = BlogContentType.objects.get(
	        id=request.session['content_info_id']
    )
	#print((request.session['content_info_id'], content_info_obj))
	form = find_class('blogging.custom.'+content_info_obj.__str__().lower(),str(content_info_obj).capitalize()+'Form' )

	if request.method == "POST":
		post_form = form(reverse('blogging:create-post'),data=request.POST.copy())
		action = request.POST.get('submit')
		if post_form.is_valid():
			post = request.POST.copy()
			if content_info_obj.is_leaf:
				blog = BlogContent()
				blog.section = post_form.cleaned_data["section"]
				blog.publication_start = None
			else:
				blog = BlogParent()
				blog.parent = post_form.cleaned_data["parent"]
			blog.title = post_form.cleaned_data["title"]
			blog.author_id = request.user
			blog.content_type = content_info_obj
			blog.slug = slugify(blog.title)
			if action == 'Publish':
				blog.data = post_form.save(post,commit=True)
				# send an email to administrator for reviewing
				# for now change the special_flag to False TODO integrate it in project management App
				blog.special_flag = False
			elif action == 'Save Draft':
				# for now change the special_flag to True TODO integrate it in project management App
				blog.special_flag = True
				blog.data = post_form.save(post)

			if use_reversion:
				with reversion.create_revision():
					blog.save()
					if content_info_obj.is_leaf:
						#print("LOGS: tags are ", post_form.cleaned_data['tags'])
						blog.tags.add(*post_form.cleaned_data['tags'])
					reversion.set_user(request.user)
					reversion.set_comment("Created first draft")
			else:
				blog.save()
				if content_info_obj.is_leaf:
					#print("LOGS: tags are ", post_form.cleaned_data['tags'])
					blog.tags.add(*post_form.cleaned_data['tags'])

			if action == 'Publish':
				generate_event.send(sender = blog.__class__, event_label = "blogging_content_submit",
								user = request.user, source_content_type = ContentType.objects.get_for_model(blog), source_object_id= blog.pk)

			del request.session['content_info_id']
			return HttpResponseRedirect(blog.get_absolute_url())

	else:
		initial = {'pid_count': '0'}
		post_form = form(reverse('blogging:create-post'),initial=initial)
	context = {'form':post_form}
	return render( request,
	    "blogging/create_page.html",
	    context)

@login_required
@group_required('Administrator','Editor','Author')
def edit_post(request,post_id):
	"""
	Used for editing existing post depending upon the post_id in the request.
	SAVE -- Save the content as draft for later revision. todo:
	SUBMIT -- Submit the post for moderation and publication.
	"""
	try:
		blog = BlogContent.objects.get(pk=post_id)
		request.session['content_info_id'] = blog.content_type.id
		#print("LOGS: EDIT ", blog.__str__())
		form = find_class('blogging.custom.'+blog.content_type.__str__().lower(),str(blog.content_type).capitalize()+'Form' )
		#print("LOGS: ContentType ", blog.content_type.__str__().lower())
		if request.method == "POST":
			post_form = form(reverse('blogging:edit-post',args = (post_id,)),data=request.POST.copy(),instance=blog)
			action = request.POST.get('submit')

			if post_form.is_valid():
				post = request.POST.copy()
				blog.title = post_form.cleaned_data["title"]
				blog.section = post_form.cleaned_data["section"]
# 				blog.author_id = request.user
				blog.slug = slugify(blog.title)
				if action == 'Publish':
					blog.data = post_form.save(post,commit=True)
					# for now change the special_flag to False TODO integrate it in project management App
					blog.special_flag = False

				elif action == 'Save Draft':
					blog.data = post_form.save(post)
					# for now change the special_flag to False TODO integrate it in project management App
					blog.special_flag = True

				# create the reversion for version control and revert back the deleted post
				if use_reversion:
					with reversion.create_revision():
						blog.save()
						#print("LOGS: tags are ", post_form.cleaned_data['tags'])
						blog.tags.set(tags= list(post_form.cleaned_data['tags']))
						reversion.set_user(request.user)
						reversion.set_comment("Saving the Blog Content changes...")
				else:
					blog.save()
					#print("LOGS: tags are ", post_form.cleaned_data['tags'])
					blog.tags.set(tags= list(post_form.cleaned_data['tags']))

				if action == 'Publish':
					generate_event.send(sender = blog.__class__, event_label = "blogging_content_submit", user = request.user, source_content_type = ContentType.objects.get_for_model(blog), source_object_id= blog.pk)

				return HttpResponseRedirect(blog.get_absolute_url())
		else:
			wrapper_form_class = find_class('blogging.custom.'+blog.content_type.__str__().lower(),str(blog.content_type).capitalize()+'Form')
			#print("LOGS: Wrapper Form Class ", wrapper_form_class)
			#print("LOGS: Content Class ", blog)
			post_form = wrapper_form_class(reverse('blogging:edit-post',args = (post_id,)),instance=blog)

		context = {'form':post_form}
		return render(request,
		    "blogging/create_page.html", context)
	except BlogContent.DoesNotExist:
		print("Unexpected error:", sys.exc_info()[0])
		for frame in traceback.extract_tb(sys.exc_info()[2]):
			fname,lineno,fn,text = frame
			print("Error in %s on line %d" % (fname, lineno))
		raise Http404

@login_required
@group_required('Administrator')
def edit_section(request,section_id):
	"""
	Used for editing existing sections depending upon the section_id in the request.
	SUBMIT -- Submit the changes made in section.
	"""
	try:
		section = BlogParent.objects.get(pk=section_id)
		form = find_class('blogging.custom.'+section.content_type.__str__().lower(),str(section.content_type).capitalize()+'Form' )
		#print("LOGS: ContentType ", section.content_type.__str__().lower())
		if request.method == "POST":
			post_form = form(reverse('blogging:edit-section',args = (section_id,)),request.POST)
			action = request.POST.get('submit')

			if post_form.is_valid():
				post = request.POST.copy()
				section.title = post_form.cleaned_data["title"]
				section.parent = post_form.cleaned_data["parent"]
				section.slug = slugify(section.title)
				if action == 'Publish':
					section.data = post_form.save(post,commit=True)

				elif action == 'Save Draft':
					section.data = post_form.save(post)
				# create the reversion for version control and revert back the deleted post
				if use_reversion:
					with reversion.create_revision():
						section.save()
						reversion.set_user(request.user)
						reversion.set_comment("Saving the Blog Content changes...")
				else:
					section.save()

				return HttpResponseRedirect(section.get_absolute_url())

		else:
			wrapper_form_class = find_class('blogging.custom.'+section.content_type.__str__().lower(),str(section.content_type).capitalize()+'Form')
			## This is bug as we dont't know the structure of form so we should pass the instance rather than initial value
			post_form = wrapper_form_class(reverse('blogging:edit-section',args = (section_id,)),instance=section)

		context = {'form':post_form}
		return render(request,
		    "blogging/create_page.html",
		    context)
	except:
		print("Unexpected error:", sys.exc_info()[0])
		for frame in traceback.extract_tb(sys.exc_info()[2]):
			fname,lineno,fn,text = frame
			print("Error in %s on line %d" % (fname, lineno))
		raise Http404

@login_required
@group_required('Administrator')
def add_new_model(request, model_name):
	if (model_name.lower() == model_name):
		normal_model_name = model_name.capitalize()
	else:
		normal_model_name = model_name
	#print(normal_model_name)
	if normal_model_name == 'ContentType' :

		if not request.user.is_staff:
			# return permission denied
			return HttpResponse(status=403)

		FieldFormSet = formset_factory(FieldTypeForm,extra=1)
		if request.method == 'POST':
			form1 = ContentTypeCreationForm(request.POST)
			form2 = FieldFormSet(request.POST)
			if form1.is_valid() and form2.is_valid():
				try:
					form_dict = {}
					for form in form2:
						#print(form.cleaned_data)
						form_dict[form.cleaned_data['field_name']] = form.cleaned_data['field_type']
					#print("LOGS: Printing fomr dictionary: ", form_dict)
					if (create_content_type(slugify_name(form1.cleaned_data['content_type']),form_dict,form1.cleaned_data['is_leaf']) == False ):
						raise forms.ValidationError("something got wronged")
					new_obj = form1.save() #TODO many things
					#print(new_obj.content_type)
				except forms.ValidationError:
					new_obj = None
				if new_obj:
					return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                	(escape(new_obj._get_pk_val()), escape(new_obj)))
				else:
					page_context = {'form1': form1,'formset':form2,  'field': normal_model_name}
					return render(request,'blogging/includes/add_content_type.html', page_context)
			else:
				#print("form is not valid form1 ", form1.is_valid(), " form 2 ", form2.is_valid())
				page_context = {'form1': form1,'formset':form2,  'field': normal_model_name}
				return render(request, 'blogging/includes/add_content_type.html', page_context)

		else:
			form = ContentTypeCreationForm()
			formset = FieldFormSet()
			#print(form.as_table())
			page_context = {'form1': form,'formset':formset,  'field': normal_model_name }
			return render(request, 'blogging/includes/add_content_type.html', page_context)


def section_index(request, slug=None):
	"""
	Main view method of blogging app. Vanilla requests to sections land up here.

	@note This does NOT give the blogcontent children of sections, but the
	hierarchy of sections.
	"""
	current_section = None
	section = None

	template = loader.get_template('blogging/section.html')
	max_entry = getattr(settings, 'BLOGGING_MAX_ENTRY_PER_PAGE', 10)

	if slug != None and len(slug) > 0:
		current_section = slug.split('/')[-1]
		if len(slug.split('/')[-1])==0:
			current_section = slug.split('/')[-2]
		#print(("Printing slug {slug}".format(slug=slug)))
		logger.debug("Printing slug {slug}".format(slug=slug))

	if current_section != None:
		try:
			section = BlogParent.objects.get(slug = str(current_section))
			#print(section)
			if request.GET.get('edit',None) == 'True':
				return HttpResponseRedirect(reverse('blogging:edit-section',
														args = (section.id,)))
			nodes = section.get_children()
		except (BlogParent.DoesNotExist):
			logger.error("Unexpected error: {val}".format(val= sys.exc_info()[0]))
			for frame in traceback.extract_tb(sys.exc_info()[2]):
				fname,lineno,fn,text = frame
				print(("Error in %s on line %d" % (fname, lineno)))
			raise Http404
	else:
		nodes = BlogParent.objects.filter(level=0)

	if nodes != None:
		paginator = Paginator(nodes, max_entry,orphans=3)
		page = request.GET.get('page')
		try:
			pages = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pages = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pages = paginator.page(paginator.num_pages)

		if section != None:
			context = {
					   'parent': section,
                       'nodes': pages,
                       'page': {'title':section.title,
								'tagline':''},
                       'max_entry': max_entry,
                     }
		else:
			context = {
						   'parent': None,
                           'nodes': pages,
                           'page': {'title':'Catalogue',
									'tagline':''},
                           'max_entry': max_entry,
                       }
	else:
		if section != None:
			#This case should be made unhittable
			context = {
					   'parent': section,
                       'nodes': None,
                       'page': {'title':section.title,
								'tagline':''},
                       'max_entry': max_entry,
                      }
		else:
			context = {
					   'parent': None,
                       'nodes': None,
                       'page': {'title':'Catalogue',
								'tagline':''},
                       'max_entry': max_entry,
                      }

	return HttpResponse(template.render(context, request))


def authors_list(request):
	return HttpResponse("Hi This is author list view ")

def author_post(request,slug,post_id):
	return HttpResponse("Hi This is author post view")

def archive(request):
	return HttpResponse("Hi This is archive view")

def teaser(request,slug=None):
	"""
	This is the blogroll method which displays the summary of entries in the
	section requested.
	"""
	max_entry = getattr(settings, 'BLOGGING_MAX_ENTRY_PER_PAGE', 10)
	try:
		current_section = slug.split("/")[-1]
		logger.debug("Printing slug {slug}".format(slug=slug))
		#print(('slug is {slug}'.format(slug=slug)))
	except (AttributeError):
		#Show all posts sorted by publish date.
		template = loader.get_template('blogging/teaser.html')
		nodes = get_posts_for_section().order_by('-publication_start')

		paginator = Paginator(nodes, max_entry,orphans=3)
		page = request.GET.get('page')
		try:
			pages = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pages = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pages = paginator.page(paginator.num_pages)
		context = {
					'parent':None,
                    'nodes': pages,
                    'page': {'title':settings.SITE_TITLE,
							'tagline':settings.SITE_TAGLINE,
							'image': None
							},
                    'max_entry': max_entry,
                   }
		return HttpResponse(template.render(context, request))

	try:
		section = BlogParent.objects.get(slug = str(current_section))
	except (BlogParent.DoesNotExist):
		logger.error("Unexpected error:{val}".format(val= sys.exc_info()[0]))
		print(traceback.format_exc())
		for frame in traceback.extract_tb(sys.exc_info()[2]):
			fname,lineno,fn,text = frame
			logger.error("Error in %s on line %d" % (fname, lineno))
			print(("Error in %s on line %d" % (fname, lineno)))
		raise Http404

	#Have a section. Get its contents
	template = loader.get_template('blogging/teaser.html')

	if request.GET.get('strict', None) == None:
		nodes = get_posts_for_section(section)
	else:
		nodes = BlogContent.published.filter(section=section)

	if nodes != None:
		paginator = Paginator(nodes, max_entry,orphans=3)
		page = request.GET.get('page', None)
		try:
			pages = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pages = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pages = paginator.page(paginator.num_pages)
	else:
		pages = None

	context = {
			   'parent':section,
               'nodes': pages,
               'page': {'title':section.title,
						'tagline':settings.SITE_TAGLINE,
						'image': section.get_image_url()
						},
               'max_entry': max_entry,
              }
	return HttpResponse(template.render(context, request))


def detail(request, slug, post_id):
	current_url = request.get_full_path()
	try:
		post_id = int(post_id)
		logger.debug("This is Detail page")

		if request.GET.get('edit',None) == 'True':
			return HttpResponseRedirect(reverse('blogging:edit-post',args = (post_id,)))

		try:
			blogs = BlogContent.objects.get(pk=post_id)
		except BlogContent.DoesNotExist:
			print('Did not find.')
			raise Http404

		if blogs.is_published() == False and request.user.is_staff == False:
			print('Not published')
			raise Http404

		template = loader.get_template('blogging/includes/'+ blogs.content_type.__str__().lower() + '.html')
		try:
			json_obj = json.loads(blogs.data)
			# Instantiate the Meta class
			description = strip_tags(list(json_obj.values())[0])
			meta = Meta(title = blogs.title,
						description = blogs.get_summary(),
						section= blogs.section.title,
						url = blogs.get_absolute_url(),
						image = blogs.get_image_url(),
						author = blogs.author_id,
						date_time = blogs.publication_start ,
						object_type = 'article',
						keywords = [ tags.name for tags in blogs.tags.all()],
						)

			json_obj['title'] = blogs.title
			json_obj['edit'] = reverse('blogging:edit-post',args = (post_id,))
			json_obj['author'] = blogs.author_id
			json_obj['published'] = blogs.published_flag

			patch_html = ""
			if use_reversion:
				available_versions = reversion.get_for_object(blogs)
				if len(available_versions) > 1 :
					new_version = available_versions[0]
					old_version = available_versions[1]
					patch_html = generate_diffs(old_version, new_version, "data",cleanup="semantic")
		except:
# 			log.user(self.request, "~SN~FRFailed~FY to fetch ~FGoriginal text~FY: Unexpected error '{0}'".format(sys.exc_info()[0]),logger)
			print(("Unexpected error:", sys.exc_info()[0]))
			for frame in traceback.extract_tb(sys.exc_info()[2]):
				fname,lineno,fn,text = frame
# 				logging.error("~SN~FRError~FY in %s on line ~FG%d~FY" % (fname, lineno),logger)
				logger.error("Error in %s on line %d" % (fname, lineno))
				print(("Error in %s on line %d" % (fname, lineno)))
			raise Http404

		context = {
					   'parent': blogs.section,
                       'nodes': blogs,
                       'content':json_obj,
                       'page': {'title':settings.SITE_TITLE,
								'tagline':settings.SITE_TAGLINE
								},
                       'patch': patch_html,
                       'meta' : meta,
                       'can_edit':(not blogs.published_flag) and
                   				  blogs.author_id == request.user ,
                  }
		return HttpResponse(template.render(context, request))

	except (ValueError):
		logger.error("Unexpected error: {val}".format(val=sys.exc_info()[0]))
		for frame in traceback.extract_tb(sys.exc_info()[2]):
			fname,lineno,fn,text = frame
			logger.error("Error in %s on line %d" % (fname, lineno))
		raise Http404

def get_posts_for_section(section=None):
	"""
	Traverse the tree hierarchy for the section and return the posts for all
	the descendents.
	"""
	if section != None:
		children = section.get_descendants(include_self=True)
		qs = Q()
		for child in children:
			qs |= Q(section=child)
		posts = BlogContent.published.filter(qs)
	else:
		posts = BlogContent.published.all()
	return posts

def tagged_post(request,tag):
	try:
		posts = BlogContent.objects.filter(tags__slug = tag)
		max_entry = getattr(settings, 'BLOGGING_MAX_ENTRY_PER_PAGE', 3)

		page = request.GET.get('page')
		paginator = Paginator(posts, max_entry)
		try:
			pages = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pages = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pages = paginator.page(paginator.num_pages)

		template = loader.get_template('blogging/teaser.html')
		context = {
                                       'nodes': pages,
                                       'page': {'title':tag, 'tagline':'We learn from stolen stuff'},
                                       'max_entry': max_entry,
                                      }
		return render(request, 'blogging/teaser.html', context)
	except ObjectDoesNotExist:
		raise Http404

def ContactUs(request):
	contact_type = request.GET.get('contact_type',None)
	name = ''
	email = ''
	if request.user.is_authenticated:
		User = request.user
		name = User.profile.get_profile_name()
		email = User.profile.get_email()

	if contact_type == None:
		contact_type = 'Queries'

	if request.method == 'POST':
		form = ContactForm(data=request.POST)
		if form.is_valid():
			subject = 'Contact mail from Aesthetic Blasphemy( ' + form.cleaned_data['contact_type'] + ' )'
			message = 'Name: ' + form.cleaned_data['name'] + '\n' + 'email: ' + form.cleaned_data['email'] + '\n Body: ' + form.cleaned_data['content']
			mail_admins(subject, message, fail_silently=True)
			template = loader.get_template('blogging/contact_page.html')
			form = ContactForm()
			context = {'success':True, 'form':form}
			return render(request,'blogging/contact_page.html',  context)
		else:
			print("LOGS:: error in Contact form")
	else:
		form = ContactForm(initial={'contact_type':contact_type,'name': name, 'email': email})
	template = loader.get_template('blogging/contact_page.html')
	context = {'form': form}
	return render(request, 'blogging/contact_page.html',context)

def BuildIndex(request):
	#if request.is_ajax():
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		template = loader.get_template('blogging/includes/index.html')
# 		course = BlogParent.objects.get(title='Course')
		section = None
		try:
			parent  = request.GET.get('section',None)
			#print("Parent id from request ", parent)
			if parent:
				section = BlogParent.objects.get(pk=parent)
		except:
			section = None

		context = {
# 	                     'nodes': course.get_descendants(include_self=True),
			'nodes': BlogParent.objects.filter(~Q(title="Orphan")),
	                                       'active': section
	                                      }
		return HttpResponse(template.render(context))
	else:
		raise Http404


def testCase(request):
	template = loader.get_template('index_tree.html')
	course = BlogParent.objects.get(title='Course')
	Django = BlogParent.objects.get(title='Computer Science')

	context = RequestContext(request, {
                                       'nodes': course.get_descendants(include_self=True),
                                       'active': Django
                                      })
	return HttpResponse(template.render(context))
#
#
#
# 	try:
# 		migrate()
# 		return render_to_response('blogging/Test_page.html', {}, context_instance=RequestContext(request))
# 	except:
# 		print "Unexpected error:", sys.exc_info()[0]
# 		for frame in traceback.extract_tb(sys.exc_info()[2]):
# 			fname,lineno,fn,text = frame
# 			print "Error in %s on line %d" % (fname, lineno)
# 		raise Http404



@group_required('Administrator')
def manage(request):
	"""
	Manage the articles; only available to administrators
	"""
	try:
		if request.method == "POST":
			action = request.POST.get('action')
			pks = request.POST.getlist("selection")
			if len(pks):
#				 print "LOGS: " + pks
				objs = BlogContent.objects.filter(pk__in=pks)

				if action == 'Publish':
					#print("LOGS: Promote the given articles")
					for obj in objs:
						if obj.published_flag != True:
							obj.published_flag = True
							obj.publication_start = datetime.datetime.now()
							obj.save()
				elif action == 'Unpublish':
					#print("LOGS: Unpublish the given articles")
					for obj in objs:
						if obj.published_flag != False:
							obj.published_flag = False
							obj.publication_start = None
							obj.save()
				elif action == 'Delete':
					for obj in objs:
						obj.delete()
		articles = BlogContent.objects.all()
		page = request.GET.get('page')
		#print('Page {}'.format(page))
		size= request.GET.get('size', 15)
		size = int(size)
		paginator = Paginator(articles, size, orphans=30)
		try:
			pages = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pages = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pages = paginator.page(paginator.num_pages)
		actions = [{"name":"Publish", "help":"Promote selected articles"},
				   {"name":"Unpublish", "help":"Unpublish selected articles"},
				   {"name":"Delete", "help":"Delete selected articles"},
				   ]
		context = {"articles": pages,
				   "actions": actions,
				   "max_entry": getattr(settings, 'BLOGGING_MAX_ENTRY_PER_PAGE', 10),
				   }

		template = loader.get_template("blogging/manage.html")
		return HttpResponse(template.render(context, request))
	except OperationalError as exp:
		print((exp.__cause__))
		print(("Unexpected error:", sys.exc_info()[0]))
		for frame in traceback.extract_tb(sys.exc_info()[2]):
			fname,lineno,fn,text = frame
			print(("Error in %s on line %d" % (fname, lineno)))
		return Http404
	except:
		print(("Unexpected error:", sys.exc_info()[0]))
		for frame in traceback.extract_tb(sys.exc_info()[2]):
			fname,lineno,fn,text = frame
			print(("Error in %s on line %d" % (fname, lineno)))
		return Http404
