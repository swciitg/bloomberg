import string
import random
import json
import urllib
import datetime
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from passlib.hash import pbkdf2_sha256
from .models import UserDetail, Session
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from blogs.models import Blog
from .forms import LoginForm, SignUpForm
# Create your views here.

def login(request):
	if request.session.has_key('eid'):
		email=request.session['eid']
		try:
			user=UserDetail.objects.get(emailID = email)
		except UserDetail.DoesNotExist:
			return HttpResponseRedirect(reverse('main:logout'))
		return HttpResponseRedirect(reverse('main:index',args=()))

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
			)
			if users.isAdmin:
				return HttpResponseRedirect(reverse('blogs:admindash',args=()))
			return HttpResponseRedirect(reverse('blogs:userdash',args=()))
	else:
		login_form = LoginForm();

	context = {
		'form' : login_form ,
	}

	return render(request , 'main/login.html' , context)

def signup(request):
	if request.session.has_key('eid'):
		 return HttpResponseRedirect(reverse('main:index',args=()))


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

			return HttpResponseRedirect(reverse('main:index',args=()))
	else:
		signup_form = SignUpForm();

	context = {
		'form' : signup_form ,
	}

	return render(request , 'main/signup.html' , context)

def logout(request):
	try:
		del request.session['eid']
	except KeyError:
		pass
	return HttpResponseRedirect(reverse('main:index',args=()))


def permissiondenied(request):
	return render(request, 'main/permdenied.html')

def index (request):
	user = ''
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		try:
			user = UserDetail.objects.get(emailID = emailID)
		except UserDetail.DoesNotExist:
			HttpResponseRedirect(reverse('main:logout'))	

	blog_latest = Blog.objects.filter(isLive = True)[:4]
	blog_featured_crousal =Blog.objects.filter(isLive = True).order_by('-views')[:5]
	blog_featured =Blog.objects.filter(isLive = True).order_by('-views')[:6]
	email = 'glorify@iitg.ac.in'


	context ={
		'user' : user,
		'blog_latest' : blog_latest,
		'blog_featured_crousal' : blog_featured_crousal,
		'blog_featured' : blog_featured,
		'email' : email,
	}

	return render(request , 'main/index.html' , context)

def about(request):
	return render(request , 'main/about_us.html')
