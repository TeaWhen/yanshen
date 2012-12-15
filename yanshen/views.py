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
# p = Pinyin()
# In [5]: p.get_pinyin(u"上海", ' ')
# Out[5]: 'shang hai'
# In [6]: p.get_initials(u"上")
# Out[6]: 'S'

@render_to('welcome.html')
def welcome(request):
    if request.user.is_authenticated():
        return redirect('/')
    appname = u"延伸"
    pagename ='welcome'
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
                    user.contact_info = json.JSONEncoder().encode({"next_id":2, "data":[{"info_id":1, "type":"Email", "key": u"电子邮箱", "value": user.email}]})
                    user.save()
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
    appname = u"延伸"
    pagename = 'index'
    users = Profile.objects.all()
    return locals()

@render_to('contact.html')
@login_required(login_url='/welcome/')
def contact(request, pk):
    appname = u"延伸"
    pagename = 'contact'
    user = Profile.objects.get(pk=pk)
    socials = user.conns.all()
    contact_info = json.JSONDecoder().decode(user.contact_info)['data']

    return locals()

@render_to('me.html')
@login_required(login_url='/welcome/')
def me(request):
    appname = u"延伸"
    pagename = 'me'
    user = request.user
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'add':
            key = request.POST['key']
            if key == '':
                key = request.POST['key_custom']
            value = request.POST['value']
            type = request.POST['type']
            contact_info = json.JSONDecoder().decode(user.contact_info)
            info_id = contact_info['next_id']
            contact_info['next_id'] += 1
            contact_info['data'].append(dict(info_id=info_id, key=key, value=value, type=type))
            user.contact_info = json.JSONEncoder().encode(contact_info)
            user.save()
            cats = user.cats.all()
            for c in cats:
                cp = json.JSONDecoder().decode(c.privilege)
                cp[str(info_id)] = False
                c.privilege = json.JSONEncoder().encode(cp)
                c.save()
        elif action == 'delete':
            info_id = int(request.POST['info_id'])
            contact_info = json.JSONDecoder().decode(user.contact_info)
            for x in contact_info['data']:
                if x['info_id'] == info_id:
                    contact_info['data'].remove(x)
                    break
            user.contact_info = json.JSONEncoder().encode(contact_info)
            user.save()
            cats = user.cats.all()
            for c in cats:
                cp = json.JSONDecoder().decode(c.privilege)
                cp.pop(str(info_id))
                c.privilege = json.JSONEncoder().encode(cp)
                c.save()
        else:
            pass
    socials = user.conns.all()
    contact_info = json.JSONDecoder().decode(user.contact_info)['data']
        
    return locals()

@render_to('group.html')
@login_required(login_url='/welcome/')
def group(request):
    appname = u"延伸"
    pagename = 'group'
    user = request.user
    categories = Category.objects.filter(owner=user)
    data = []
    for category in categories:
        data.append(dict(category=category, friends=Relationship.objects.filter(from_id=user.id,cat_id=category)))
    #user.
    return locals()

@render_to('group_setting.html')
@login_required(login_url='/welcome/')
def group_settings(request, pk):
    return locals()

@render_to('index.html')
@login_required(login_url='/welcome/')
def group_detail(request, gid):
    appname = u"延伸"
    cat = Category.objects.get(pk=gid)
    users = []
    for rl in cat.relationship_set.all():
        users.append(rl.to_id)
    return locals()

@render_to('map.html')
@login_required(login_url='/welcome/')
def map(request):
    appname = u"延伸"
    pagename = 'map'
    users = Profile.objects.all()
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
