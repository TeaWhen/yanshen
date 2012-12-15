from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response, RequestContext
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import time

def welcome(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				next = request.POST['next']
				return redirect(next)
			else:
				message = 'disabled account'
				return render_to_response('welcome.html', locals(), context_instance=RequestContext(request))
		else:
			message = 'invalid login'
			return render_to_response('welcome.html', locals(), context_instance=RequestContext(request))
	else:
		try:
			next = request.POST['next']
		except:
			next = '/'
		return render_to_response('welcome.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/welcome/')
def index(request):
	users = Profile.objects.all()
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/welcome/')
def contact(request, pk):
	user = Profile.objects.get(pk=pk)
	return render_to_response('contact.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/welcome/')
def me(request):
	user = request.user
	return render_to_response('me.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/welcome/')
def group(request):
	return render_to_response('group.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/welcome/')
def map(request):
	return render_to_response('map.html', locals(), context_instance=RequestContext(request))

def page_not_found(request):
	return render(request, '404.html')

def robots(request):
	return render(request, 'robots.txt', content_type="text/plain")

def humans(request):
	return render(request, 'humans.txt', content_type="text/plain")

def orca(request):
	return HttpResponse("b5da7f1e4f9066c4", content_type="text/plain")
