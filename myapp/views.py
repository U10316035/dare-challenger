from django.shortcuts import render

from .models import Post
from .forms import AddPost
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
	if request.method == 'GET':
		post_list = Post.objects.all()
		return render(request,"myapp/index.html",
			{'posts': post_list})
	if request.method == 'POST':
		django_form = AddPost(request.POST)
		if django_form.is_valid():
			new_post_text = django_form.data.get("text")
			Post.objects.create(text = new_post_text,)
			return HttpResponseRedirect("/")
def bulletinboard(request):
	return render(request, 'myapp/bulletinboard.html', {})

def challenge(request):
	return render(request, 'myapp/challenge.html', {})

def about(request):
	return render(request, 'myapp/about.html', {})

def gauntlet(request):
	return render(request, 'myapp/gauntlet.html', {})

def login(request):
	return render(request, 'myapp/login.html', {})
