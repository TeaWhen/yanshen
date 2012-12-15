# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response, RequestContext
from users.models import Profile, Category, Relationship
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from annoying.decorators import render_to
from django.core.exceptions import ValidationError
from xpinyin import Pinyin
import json

# json.JSONEncoder().encode()
# json.JSONDecoder().decode()

@render_to('welcome.html')
def welcome(request):
	if request.user.is_authenticated():
		return redirect('/')
	appname = "延伸"
	pagename ='welcome'
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		action = request.POST['action']
		if action == 'login':
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					p = Pinyin()
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
	pagename = 'index'
	users = Profile.objects.all()
	return locals()

@render_to('contact.html')
@login_required(login_url='/welcome/')
def contact(request, pk):
	appname = "延伸"
	pagename = 'contact'
	user = Profile.objects.get(pk=pk)
	socials = user.conns.all()
	icon_name = {
		'weibo': "icon-weibo",
		'renren': "icon-renren",
		'github': "icon-github",
		'facebook': "icon-facebook",
		'tqq': "icon-tenxunweibo",
		'jiepang': "icon-jiepang"
	}
	social_url = {
		'weibo': "http://weibo.com/",
		'renren': "http://renren.com/",
		'github': "http://github.com/",
		'facebook': "http://facebook.com",
		'tqq': "http://t.qq.com/",
		'jiepang': "http://jiepang.com/"
	}
	for s in socials:
		s.url = social_url[s.type]
		s.icon = icon_name[s.type]

	contact_info = json.JSONDecoder().decode(user.contact_info)['data']

	return locals()

@render_to('me.html')
@login_required(login_url='/welcome/')
def me(request):
	appname = "延伸"
	pagename = 'me'
	user = request.user
	if request.method == 'POST':
		action = request.POST['action']
		if action == 'add':
			key = request.POST['key']
			value = request.POST['value']
			type = request.POST['type']
			contact_info = json.JSONDecoder().decode(user.contact_info)
			info_id = contact_info['next_id']
			contact_info['next_id'] += int(contact_info['next_id']) + 1
			contact_info['data'].append(dict(info_id=info_id, key=key, value=value, type=type))
			user.contact_info = json.JSONEncoder().encode(contact_info)
			user.save()
		else:
			pass
	socials = user.conns.all()
	icon_name = {
		'weibo': "icon-weibo",
		'renren': "icon-renren",
		'github': "icon-github",
		# 'facebook': "icon-facebook",
		'tqq': "icon-tenxunweibo",
		'jiepang': "icon-jiepang"
	}
	social_url = {
		'weibo': "http://weibo.com/",
		'renren': "http://renren.com/",
		'github': "http://github.com/",
		# 'facebook': "http://facebook.com",
		'tqq': "http://t.qq.com/",
		'jiepang': "http://jiepang.com/"
	}
	for s in socials:
		s.url = social_url[s.type]
		s.icon = icon_name[s.type]

	contact_info = json.JSONDecoder().decode(user.contact_info)['data']
		
	return locals()

@render_to('group.html')
@login_required(login_url='/welcome/')
def group(request):
	appname = "延伸"
	pagename = 'group'
	user = request.user
	categories = Category.objects.filter(owner=user)
	data = []
	for category in categories:
		data.append(dict(category=category, friends=Relationship.objects.filter(from_id=user.id,cat_id=category)))
	#user.
	return locals()

@render_to('map.html')
@login_required(login_url='/welcome/')
def map(request):
	appname = "延伸"
	pagename = 'map'
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
