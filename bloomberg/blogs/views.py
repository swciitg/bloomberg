import string
import random
import json
import urllib
import datetime
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from .forms import BlogUploadForm
from passlib.hash import pbkdf2_sha256
from main.models import UserDetail , Session
from .models import Blog , Comment
from django.urls import reverse
from django.contrib import messages

# Create your views here.

def userdash (request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		if not UserDetail.objects.filter(emailID__exact = emailID):
			return HttpResponseRedirect(reverse('main:login'))
		user = UserDetail.objects.get(emailID = emailID)
		if user.isBlocked:
			return HttpResponseRedirect(reverse('blogs:permissiondenied'))
		blogs = Blog.objects.filter(authorID__exact = user.userID)
		live=0
		notlive=0
		for blog in blogs:
			if blog.isLive:
				live=live+1
			else:
				notlive=notlive+1
		context = {
			'user' : user,
			'blogs' : blogs,
			'live' : live,
			'notlive': notlive,
		}
		return render(request , 'blogs/userdash.html' , context)

	return HttpResponseRedirect(reverse('main:login'))

def admindash (request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		blogs = Blog.objects.filter(isLive=True)
		page_title = 'ALL POSTS'
		context = {
			'user' : user ,
			'blogs' : blogs ,
			'page_title' : page_title,
		}

		return render(request , 'blogs/admindash.html' , context)

	return HttpResponseRedirect(reverse('main:login'))


def newpost(request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		page_title='NEW POSTS'
		blogs = Blog.objects.all().order_by('-createdAt')
		context = {
			'user' : user ,
			'blogs' : blogs ,
			'page_title' : page_title,
		}

		return render(request , 'blogs/admindash.html' , context)

	return HttpResponseRedirect(reverse('main:login'))


def blog(request , pk):
	blog = get_object_or_404(Blog , pk=pk)
	str= blog.blogID
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if user.isBlocked:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		if not blog.isLive:
			if not blog.authorID == user.userID:
				return HttpResponseRedirect(reverse('main:index'))
			else:
				author = user
				context = {
					'blog' : blog,
					'author' : author,
				}
				return render(request, 'blogs/blog.html' , context)
		else:
			if blog.authorID == user.userID:
				pass
			else:
					str = str + emailID
					if not request.session.has_key(str):
						request.session[str]=1
						blog.views = F('views') + 1
						blog.save()
					else:
						pass
	else:
		if not request.session.has_key(str):
			request.session[str]=1
			blog.views = F('views') + 1
			blog.save()
		else:
			pass

	author = UserDetail.objects.get(userID = blog.authorID)
	context = {
		'blog' : blog,
		'author' : author,
	}

	return render(request, 'blogs/blog.html' , context)

def pendingpost(request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		blogs = Blog.objects.filter(isLive=False)
		print(blogs)
		page_title='PENDING POSTS'
		context = {
			'user' : user ,
			'blogs' : blogs ,
			'page_title' : page_title,
		}
		return render(request , 'blogs/admindash.html' , context)

def blogUpload(request):
	if request.method == 'POST':
		if request.session.has_key('eid'):
			emailID = request.session['eid']
			user = UserDetail.objects.get(emailID = emailID)
			blog_form = BlogUploadForm(request.POST, request.FILES)
			title = request.POST['title']
			image = request.FILES['image']
			content = request.POST['content']
			topic = request.POST['topic']
			tags = request.POST['tags']

			if blog_form.is_valid():
				def random_gen(size=11 , chars = string.ascii_letters + string.digits):
					return ''.join(random.choice(chars) for x in range(size))

				blogID = random_gen()

				Blog.objects.create(
					blogID = blogID,
					authorID = user.userID,
					title = title,
					image = image,
					content = content,
					topic = topic,
					name = user.name,
					tags = tags,
				)

			    # m.model_pic = form.cleaned_data['image']
				return HttpResponse('blog upload success')
		else:
			return HttpResponseRedirect(reverse('main:login'))

	else:
		blog_form = BlogUploadForm();

	context = {
		'form' : blog_form ,
	}

	return render(request , 'blogs/blogupload.html' , context)

def bloglive(request, pk):
	blog = get_object_or_404(Blog , pk=pk)
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if user.isAdmin:
			blog.isLive=True
			blog.approvedBy=user.name
			blog.save()
			return HttpResponseRedirect(reverse('blogs:pendingpost'))
		else:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
	else:
		return HttpResponseRedirect(reverse('main:login'))

def blogblock(request, pk):
	blog = get_object_or_404(Blog , pk=pk)
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if user.isAdmin:
			blog.isLive=False
			blog.approvedBy=user.name
			blog.save()
			return HttpResponseRedirect(reverse('blogs:pendingpost'))
		else:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
	else:
		return HttpResponseRedirect(reverse('main:login'))
