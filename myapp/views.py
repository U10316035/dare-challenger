#!/usr/bin/python
#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response

#from .models import Post
#from .forms import AddPost
from .forms import userForm
from .models import UserData
from .forms import detailForm
from .models import detail
from .forms import detailResponseForm
from .models import detailResponse
from .forms import challengeForm
from .models import challengeData
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.template import loader
from datetime import datetime
from django.template import RequestContext
import math
#import datetime
from django.utils import timezone
#from .mybackend import MyBackend
# Create your views here.

def index(request):
	ch = challengeData.objects.all()
	ch = sorted(ch, key=lambda x: x.mancount, reverse=True)
	cc = ch[0]
	ch = ch[1:5]
	return render_to_response('myapp/index.html', locals())
#	if request.method == 'GET':
#		post_list = Post.objects.all()
#		return render(request,"myapp/index.html",
#			{'posts': post_list})
#	if request.method == 'POST':
#		django_form = AddPost(request.POST)
#		if django_form.is_valid():
#			new_post_text = django_form.data.get("text")
#			Post.objects.create(text = new_post_text,)
#			return HttpResponseRedirect("/")

#@login_required
def error(request):
	if request.user.is_authenticated():
		return render(request, 'myapp/index.html',{})
	return render(request, 'myapp/error.html',{})

def bulletinboard(request):
	ch = challengeData.objects.all()
	ch2 = challengeData.objects.order_by('-urlnumber')
	chman = sorted(ch, key=lambda x: x.mancount, reverse=True)
	return render_to_response('myapp/bulletinboard.html', locals())

def videoForChallenge(request):
	de = detail.objects.filter(isFinish=True)
	# de.endTime = de.startTime.strftime(de_man.startTime, '%Y-%m-%d')
	# de.save()
	# de = detail.objects.all()
	dem_list = sorted(de, key=lambda x: x.mancount, reverse=True)
	# de_time = sorted(de, key=lambda x: x.startTime, reverse=True)
	# stime = datetime.strftime(de_man.startTime, '%Y-%m-%d')
	# dem_list2 = de_man[5:8]
	return render_to_response('myapp/videoForChallenge.html', locals())

def rank(request):
	#return render(request, 'myapp/rank.html', {})
	t = loader.get_template('myapp/rank.html')
	c = {}
	return HttpResponse(t.render(c,request))

def join(request,pk,un):
	if request.user.is_authenticated():
		u = challengeData.objects.filter(username=un)
		username = request.user.username
		us = detail.objects.filter(username=username,urlnumber=pk)
		if us:
			de = detail.objects.filter(username=username)
			ch = challengeData.objects.filter(username=username)
			return render_to_response('myapp/challenge.html',locals())
		else:
			ch = u.get(urlnum=pk)
			ch.mancount += 1
			det = detail.objects.create(urlnumber=pk,username=username,title=ch.title,detail=ch.detail)
			ch.save()
			det.save()
			### endTime in detail is use to save str of startTime!! ###
			dee = detail.objects.get(urlnumber=pk,username=username)
			dee.endTime = dee.startTime.strftime('%Y-%m-%d')
			dee.save()
			ch = challengeData.objects.filter(username=username)
			###-----------------------------------------------------###
# 	src = request.POST.get('vediosrc')
# 	de_curtime = datetime.strptime(datetime.now().isoformat(), '%Y-%m-%dT%H:%M:%S.%f')
# 	de_urlnum = curtime.microsecond

	de = detail.objects.filter(username=username)
	return render_to_response('myapp/challenge.html',locals())


def detailUnfinish(request ,pk ,un):
	if request.method == "GET":
		de = detail.objects.get(username=un,urlnumber=pk)
		deR = detailResponse.objects.filter(username=un,urlnumber=pk)
		ch = challengeData.objects.get(urlnum=pk)
		cur = timezone.now()
		delta = cur - de.startTime
		intdel = int(math.floor(delta.total_seconds()))
		leave_sec = ch.endTime*24*60*60 - intdel
		de.mancount += 1
		de.save()
		return render_to_response('myapp/detailUnfinish.html',RequestContext(request, locals()))
		# return render_to_response('myapp/detailUnfinish.html',locals())
	if request.POST["action"] == 'SendVedio':
		dform = detailForm(request.POST)
		vsrc = dform.data.get('videosrc')
		de = detail.objects.get(username=un,urlnumber=pk)
		embedStr = 'https://www.youtube.com/embed/'
		videosrc = embedStr+vsrc[-11:-1]+vsrc[-1]
		picfront = 'https://img.youtube.com/vi/'
		picback = '/hqdefault.jpg'
		picurl = picfront+vsrc[-11:-1]+vsrc[-1]+picback
		de.video = videosrc
		de.isFinish = True
		de.videopic = picurl
		de.save(update_fields=['video','isFinish','videopic'])
		return render_to_response('myapp/detailUnfinish.html',RequestContext(request, locals()))

	if request.POST["action"] == 'SendMessage':
		de = detail.objects.get(username=un,urlnumber=pk)
		drform = detailResponseForm(request.POST)
		response = drform.data.get('response_area')
		stime = datetime.strftime(datetime.now(), '%Y-%m-%d-%H:%M:%S')
		owner = request.user.username
		if owner ==  "" :
			owner = '訪客'
			dr = detailResponse.objects.create(detailowner=owner,username=un,urlnumber=pk,response=response,postTime=stime,whichDetail=de)
			dr.save()
			deR = detailResponse.objects.filter(username=un,urlnumber=pk)
			return render_to_response('myapp/detailUnfinish.html',RequestContext(request, locals()))
		else : 
			owner = request.user.username
			dr = detailResponse.objects.create(detailowner=owner,username=un,urlnumber=pk,response=response,postTime=stime,whichDetail=de)
			dr.save()
			deR = detailResponse.objects.filter(username=un,urlnumber=pk)
			return render_to_response('myapp/detailUnfinish.html',RequestContext(request, locals()))
		#detailowner = response.user
		# deR = detailResponse.objects.get(username=un,urlnumber=pk)
	

def detailPublicChallenge(request ,pk ,un):
	u = challengeData.objects.filter(username=un)
	ch = u.get(urlnum=pk)
	ch.mancount += 1
	ch.save()
	de = detail.objects.filter(urlnumber=pk,isFinish=True)
	t = loader.get_template('myapp/detailPublicChallenge.html')
	c = locals()
	return HttpResponse(t.render(c,request))


def readMorePage(request ,pk, un):
	u = detail.objects.filter(username=un)
	de = u.get(urlnumber=pk)
	t = loader.get_template('myapp/readMorePage.html')
	c = locals()
	return HttpResponse(t.render(c,request))

def challenge(request):
	username = request.user.username
	de = detail.objects.filter(username=username)
	ch = challengeData.objects.filter(username=username)
	return render_to_response('myapp/challenge.html',locals())

def about(request):
	return render(request, 'myapp/about.html', {})

def gauntlet(request):
	return render(request, 'myapp/gauntlet.html', {})


def makeChallenge(request):
	if request.method == "GET":
		return render(request, 'myapp/makeChallenge.html', {})

	if request.method == "POST":
		#uform = userForm(request.POST)
		cform = challengeForm(request.POST)
		curtime = datetime.strptime(datetime.now().isoformat(), '%Y-%m-%dT%H:%M:%S.%f')
		stime = datetime.strftime(datetime.now(), '%Y-%m-%d')
		urlnum = curtime.microsecond
		#username = uform.data.get('id')
		#username = User.objects.get('id')
		username = request.user.username
		title = cform.data.get('Challenge_title')
		detail = cform.data.get('Challenge_detail')
		endtime = cform.data.get('endtime')
		endsec = endtime
		cha = challengeData.objects.filter(title=title,detail=detail,username=username)
		#c = challengeData(title=title,detail=detail,urlnum=urlnum,username=username,startTime=stime)
		if cha:
			ch = challengeData.objects.all()
			ch = sorted(ch, key=lambda x: x.mancount, reverse=True)
			cc = ch[0]
			ch = ch[1:5]
			return render_to_response('myapp/index.html', locals())

		else:
			c = challengeData.objects.create(title=title,detail=detail,urlnum=urlnum,username=username,endTime=endsec)
			c.save()
			ch = challengeData.objects.all()
			ch = sorted(ch, key=lambda x: x.mancount, reverse=True)
			cc = ch[0]
			ch = ch[1:5]
			return render_to_response('myapp/index.html', locals())

def logout(request):
	auth.logout(request)
	ch = challengeData.objects.all()
	ch = sorted(ch, key=lambda x: x.mancount, reverse=True)
	cc = ch[0]
	ch = ch[1:5]
	return render_to_response('myapp/index.html', locals())
	
def login(request):
	if request.user.is_authenticated(): 
		ch = challengeData.objects.all()
		ch = sorted(ch, key=lambda x: x.mancount, reverse=True)
		cc = ch[0]
		ch = ch[1:5]
		return render_to_response('myapp/index.html', locals())
		#return render(request, 'myapp/index.html', {})

	#username = request.POST.get('username','')
	#password = request.POST.get('password','')

	uname = request.POST.get('username')
	#email = request.POST.get('mail')
	pword = request.POST.get('pass')
	
	#user = User.objects.get(email=email)
	#uname = User.objects.get(email=email).username
	user = authenticate(username=uname, password=pword)
	"""try:
		user = User.objects.get(username=uname)
	except User.DoesNotExist:
		user = None"""
	
	#user = authenticate(username='dare',password='dare')
	if user is not None:#and user.is_active:
		auth.login(request, user)
		ch = challengeData.objects.all()
		ch = sorted(ch, key=lambda x: x.mancount, reverse=True)
		cc = ch[0]
		ch = ch[1:5]
		return render_to_response('myapp/index.html', locals())
	else:
		return render(request, 'myapp/login.html', {})
	"""try:
		user = User.objects.get(username=uname)
	except User.DoesNotExist:
		user = None
	#if not uname or not pword:
	#	return HttpResponseRedirect("/")
	dform = userForm(request.POST or None)
	if dform.is_valid():
		uname = dform.data.get("username")
		pword = dform.data.get("password")
		#uname = dform.cleaned_data["username"]
		#pword = dform.cleaned_data["password"]
		user = authenticate(username=uname,password=pword)
		if user is not None:#and user.is_active:
			auth.login(request, user)
			return render(request, 'myapp/error.html', {})
		else:
			return render(request, 'myapp/login.html', {})
		#return HttpResponseRedirect("/")
	else:
		return render(request, 'myapp/login.html', {})"""
	#else:
	#	return render(request, 'myapp/bulletinboard.html', {})
	#return render(request, 'myapp/login.html', {})
	#if uname:
	#	User.objects.create(username=uname,password=pword)

	#try:
	#	user = User.objects.get(username=uname)
	#except User.DoesNotExist:
	#	user = None
	

		#if user is not None:#and user.is_active:
		#	login(request, user)
		#	return render(request, 'myapp/error.html', {})
		#else:
		#	return render(request, 'myapp/login.html', {})


def register(request):
	if request.user.is_authenticated(): 
		return render(request, 'myapp/index.html', {})

	if request.method == "GET":
		return render(request, 'myapp/register.html',{})

	if request.method == "POST":
		uform = userForm(request.POST)
	#	if uform.is_valid():
		#username = uform.cleaned_data['id']
		#password = uform.cleaned_data['password']
		#email = uform.cleaned_data['email']
		username = uform.data.get('id')
		password = uform.data.get('password')
		email = uform.data.get('email')
			#user = User.objects.get(email=email)
		error1 = False
		error2 = False
		error3 = False
		if User.objects.filter(username=username):
			error3 = True
		if User.objects.filter(email=email):
			error1 = True
		if not username or not password or not email:
			error2 = True
		if '@' not in email:
			error1 = True
		if not error1 and not error2 and not error3:
			u = User(username=username,password=password,email=email)
			u.set_password(password)
			'''user = User()
			user.username=username
			user.set_password(password)
			user.email=email
			user.save()'''
			u.save()
			user = authenticate(username=username, password=password)
			if user is not None:#and user.is_active:
				auth.login(request, user)
			ch = challengeData.objects.all()
			ch = sorted(ch, key=lambda x: x.mancount, reverse=True)
			cc = ch[0]
			ch = ch[1:5]
			return render_to_response('myapp/index.html', RequestContext(request,locals()))
			#return HttpResponse('<h1>email used</h1>')
		else:
			return render_to_response('myapp/register.html', RequestContext(request,locals()))
			#if user is not None:
			#	return render(request, 'myapp/register.html',{})
	#	else:
	#		return render(request, 'myapp/bulletinboard.html',{})
	#return render(request, 'myapp/register.html',{})
	#if 'id' not in request.POST:
	#	return render(request, 'myapp/login.html', {})
	#if not request.POST['email']:
	#	return render(request, 'myapp/login.html', {})
	#if not request.POST['password']:
	#	return render(request, 'myapp/login.html', {})
	#if 'no' in request.POST:
	#	return render(request, 'myapp/error.html', {})
	#if 'ok' in request.POST:
		#name = request.POST['id']
		#mail = request.POST['email']
		#pas = request.POST['password']
		#User.objects.create(username=name,password=pas,email=mail)
		#return render(request, 'myapp/error.html', {})
	#else:
	#	return render(request, 'myapp/login.html', {})