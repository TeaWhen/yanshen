from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response, RequestContext
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import time

from annoying.decorators import render_to

@render_to('welcome.html')
def welcome(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		action = request.POST['action']
		if action == 'login':
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					next = request.POST['next']
					return redirect(next)
				else:
					message = 'disabled account'
					return locals()
			else:
				message = 'invalid login'
				return locals()
		else:
			pass
	else:
		try:
			next = request.POST['next']
		except:
			next = '/'
		return locals()

@render_to('index.html')
@login_required(login_url='/welcome/')
def index(request):
	users = Profile.objects.all()
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

@render_to('contact.html')
@login_required(login_url='/welcome/')
def contact(request, pk):
	user = Profile.objects.get(pk=pk)
	return render_to_response('contact.html', locals(), context_instance=RequestContext(request))

@render_to('me.html')
@login_required(login_url='/welcome/')
def me(request):
	user = request.user
	return locals()

@render_to('group.html')
@login_required(login_url='/welcome/')
def group(request):
	return locals()

@render_to('map.html')
@login_required(login_url='/welcome/')
def map(request):
	return locals()

def page_not_found(request):
	return render(request, '404.html')

def robots(request):
	return render(request, 'robots.txt', content_type="text/plain")

def humans(request):
	return render(request, 'humans.txt', content_type="text/plain")

def orca(request):
	return HttpResponse("b5da7f1e4f9066c4", content_type="text/plain")
