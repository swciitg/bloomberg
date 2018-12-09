import string
import random
import json
import urllib
import datetime 
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, SignUpForm, BlogUploadForm
from passlib.hash import pbkdf2_sha256
from .models import UserDetail , Blog , Comment , Session
from django.urls import reverse
from django.contrib import messages

# Create your views here.

def index (request):
	user = ''
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)

	blog_latest = Blog.objects.filter(isLive = True)[:4]
	blog_featured_crousal =Blog.objects.filter(isLive = True).order_by('-views')[:3]
	blog_featured =Blog.objects.filter(isLive = True).order_by('-views')[:6]
	email = 'glorify@iitg.ac.in'


	context ={
		'user' : user,
		'blog_latest' : blog_latest,
		'blog_featured_crousal' : blog_featured_crousal,
		'blog_featured' : blog_featured,
		'email' : email,
	}

	return render(request , 'blogs/index.html' , context)

def login(request):
	if request.session.has_key('eid'):
		 return HttpResponseRedirect(reverse('blogs:index',args=()))

	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		emailID = request.POST['emailID']
		password = request.POST['password']
		# user = UserDetail.objects.get(pk=emailID)

		if login_form.is_valid():
			request.session['eid']=emailID
			# bloguser = UserDetail.objects.filter(emailID__exact=emailID)
			# # print (user.emailID)
			# if bloguser.isAdmin:
			# 	return HttpResponseRedirect(reverse('admindash',args=()))
			users = UserDetail.objects.get(emailID = emailID)
			Session.objects.create(
				userID = users.userID,
				name = users.name,
				emailID = users.emailID,
				logInTime = datetime.datetime.now(),
				logOutTime = None,
				isExpired = False,
			)
			if users.isAdmin:
				return HttpResponseRedirect(reverse('blogs:admindash',args=()))
			return HttpResponseRedirect(reverse('blogs:userdash',args=()))
	else:
		login_form = LoginForm();

	context = {
		'form' : login_form ,
	}

	return render(request , 'blogs/login.html' , context)

def signup(request):
	if request.session.has_key('eid'):
		 return HttpResponseRedirect(reverse('blogs:index',args=()))


	if request.method == 'POST':
		signup_form = SignUpForm(request.POST)

		name = request.POST['name']
		emailID = request.POST['emailID']
		password = request.POST['password']
		mobile = request.POST['mobile']

		enc_string = pbkdf2_sha256.encrypt(password ,rounds=100, salt_size = 32)

		def random_gen(size=7 , chars = string.ascii_letters + string.digits):
			return ''.join(random.choice(chars) for x in range(size))

		userID = random_gen()

		if signup_form.is_valid():
			''' Begin reCAPTCHA validation '''
			recaptcha_response = request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {
			    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			    'response': recaptcha_response
			}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())
			''' End reCAPTCHA validation '''

			if result['success']:
			    UserDetail.objects.create(
					name = name,
					emailID = emailID,
					password = enc_string,
					mobile = mobile,
					userID = userID,
				)
			    messages.success(request, 'New account created!')
			else:
			    messages.error(request, 'Invalid reCAPTCHA. Please try again.')

			return HttpResponseRedirect(reverse('blogs:index',args=()))
	else:
		signup_form = SignUpForm();

	context = {
		'form' : signup_form ,
	}

	return render(request , 'blogs/signup.html' , context)

def logout(request):
	try:
		del request.session['eid']
	except KeyError:
		pass
	return HttpResponseRedirect(reverse('blogs:index',args=()))

def userdash (request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		if not UserDetail.objects.filter(emailID__exact = emailID):
			return HttpResponseRedirect(reverse('blogs:login'))
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

	return HttpResponseRedirect(reverse('blogs:login'))

def admindash (request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('blogs:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('blogs:permissiondenied'))
		blogs = Blog.objects.all()
		page_title = 'ALL POSTS'
		context = {
			'user' : user ,
			'blogs' : blogs ,
			'page_title' : page_title,
		}

		return render(request , 'blogs/admindash.html' , context)

	return HttpResponseRedirect(reverse('blogs:login'))

def pendingpost(request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('blogs:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('blogs:permissiondenied'))
		blogs = Blog.objects.filter(approvedBy=None)
		print(blogs)
		page_title='PENDING POSTS'
		context = {
			'user' : user ,
			'blogs' : blogs ,
			'page_title' : page_title,
		}
		return render(request , 'blogs/admindash.html' , context)

def newpost(request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('blogs:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('blogs:permissiondenied'))
		page_title='NEW POSTS'
		blogs = Blog.objects.all().order_by('-createdAt')
		context = {
			'user' : user ,
			'blogs' : blogs ,
			'page_title' : page_title,
		}

		return render(request , 'blogs/admindash.html' , context)

	return HttpResponseRedirect(reverse('blogs:login'))


def blog(request , pk):
	blog = get_object_or_404(Blog , pk=pk)
	str= blog.blogID
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if user.isBlocked:
			return HttpResponseRedirect(reverse('blogs:permissiondenied'))
		if not blog.isLive:
			if not blog.authorID == user.userID:
				return HttpResponseRedirect(reverse('blogs:index'))
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

def permissiondenied(request):
	return render(request, 'blogs/permdenied.html')

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
			return HttpResponseRedirect(reverse('blogs:login'))

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
			return HttpResponseRedirect(reverse('blogs:permissiondenied'))
	else:
		return HttpResponseRedirect(reverse('blogs:login'))

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
			return HttpResponseRedirect(reverse('blogs:permissiondenied'))
	else:
		return HttpResponseRedirect(reverse('blogs:login'))
