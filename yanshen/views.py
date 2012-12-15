# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response, RequestContext
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from annoying.decorators import render_to
from django.core.exceptions import ValidationError

@render_to('welcome.html')
def welcome(request):
	appname = "延伸"
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		action = request.POST['action']
		if action == 'login':
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('/')
				else:
					message = '账户已被注销。'
					return locals()
			else:
				message = 'Email 或密码错误。'
				return locals()
		elif action == 'reg':
			if Profile.objects.filter(email=username).exists():
			    message = '您已经注册过了。'
			    return locals()
			else:
				try:
					user = Profile.objects.create_user(email=username, password=password)
				except ValidationError:
					message = '请输入正确的 Email 地址。'
					return locals()
				if user:
					user = authenticate(username=username, password=password)
					login(request, user)
					return redirect('/me/?first=1')
				else:
					message = '抱歉，服务器开小差了，注册失败。'
					return locals()
	else:
		return locals()

@render_to('index.html')
@login_required(login_url='/welcome/')
def index(request):
	appname = "延伸"
	users = Profile.objects.all()
	return locals()

@render_to('contact.html')
@login_required(login_url='/welcome/')
def contact(request, pk):
	appname = "延伸"
	user = Profile.objects.get(pk=pk)
	return locals()

@render_to('me.html')
@login_required(login_url='/welcome/')
def me(request):
	appname = "延伸"
	user = request.user
	return locals()

@render_to('group.html')
@login_required(login_url='/welcome/')
def group(request):
	appname = "延伸"
	return locals()

@render_to('map.html')
@login_required(login_url='/welcome/')
def map(request):
	appname = "延伸"
	return locals()

@login_required(login_url='/welcome/')
def signout(request):
	logout(request)
	return redirect('/welcome/')

def page_not_found(request):
	return render(request, '404.html')

def robots(request):
	return render(request, 'robots.txt', content_type="text/plain")

def humans(request):
	return render(request, 'humans.txt', content_type="text/plain")

def orca(request):
	return HttpResponse("b5da7f1e4f9066c4", content_type="text/plain")
