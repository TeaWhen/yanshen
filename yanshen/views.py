# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.shortcuts import render_to_response, RequestContext
from users.models import Profile, Category, Relationship, Invitation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from annoying.decorators import render_to
from django.core.exceptions import ValidationError
from xpinyin import Pinyin
import json
from django.http import Http404
from conns.views import calc_friends

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
        if username == '' or password =='' or action == '':
            message = '抱歉，服务器开小差了，注册失败。'
            return locals()
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
                    user.first_name = request.POST['firstname']
                    user.last_name = request.POST['lastname']
                    p = Pinyin()
                    user.pinyin = p.get_pinyin(user.last_name + user.first_name, ' ')
                    for char in user.last_name + user.first_name:
                        user.pinyin += get_initials(char)
                    user.contact_info = json.JSONEncoder().encode({"next_id":2, "data":[{"info_id":1, "type":"Email", "key": u"电子邮箱", "value": user.email}]})
                    user.save()
                    category = Category.objects.create(name=u'未分组', owner=user, privilege='{"1":false}')
                    category.save()
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
    relationship = Relationship.objects.filter(from_id=request.user)
    users = []
    for r in relationship:
        users.append(r.to_id)
    sorted(users, key=lambda user: user.pinyin)
    noti_count = len(request.user.invites.all())+len(request.user.pendings.all())
    return locals()

@render_to('contact.html')
@login_required(login_url='/welcome/')
def contact(request, pk):
    appname = u"延伸"
    pagename = 'contact'
    user = Profile.objects.get(pk=pk)
    socials = user.conns.all()
    contact_info = json.JSONDecoder().decode(user.contact_info)['data']
    owner = Profile.objects.get(pk=pk)

    data = []
    social_data = []
    cats = Category.objects.filter(owner=request.user)
    rl = Relationship.objects.get(from_id=request.user, to_id=owner)
    mycat = rl.cat_id

    category = Relationship.objects.get(from_id=owner, to_id=request.user).cat_id
    privilege = json.JSONDecoder().decode(category.privilege)
    for info in contact_info:
        if privilege[str(info['info_id'])] == True:
            data.append(info)
            
    for social in socials:
        if privilege[social.type+str(social.uid)] == True:
            social_data.append(social)

    locations = owner.get_locations()

    if request.method == 'POST':
        newcat = Category.objects.get(pk=request.POST['newcat'])
        rl.cat_id = newcat
        rl.save()
        mycat = newcat
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
        elif action == 'edit':
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            user.save()
    socials = user.conns.all()
    contact_info = json.JSONDecoder().decode(user.contact_info)['data']
    
    locations = request.user.get_locations()

    return locals()

@render_to('group.html')
@login_required(login_url='/welcome/')
def group(request):
    appname = u"延伸"
    pagename = 'group'
    user = request.user
    if request.method == 'POST':
        ncat = Category(name=request.POST['name'], owner=request.user)
        p = {}
        for s in ncat.owner.conns.all():
            p[s.type+str(s.uid)] = True
        contact_info = json.JSONDecoder().decode(ncat.owner.contact_info)
        for i in contact_info['data']:
            p[i['info_id']] = False
        ncat.privilege = json.JSONEncoder().encode(p)
        ncat.save()
    categories = Category.objects.filter(owner=user)
    data = []
    for category in categories:
        data.append(dict(category=category, friends=Relationship.objects.filter(from_id=user.id,cat_id=category)))
    #user.
    return locals()

@render_to('group_setting.html')
@login_required(login_url='/welcome/')
def group_settings(request, pk):
    category = Category.objects.get(pk=pk, owner=request.user)
    if category is None:
        raise Http404('Error')
    privilege = json.JSONDecoder().decode(category.privilege)
    contact_info = json.JSONDecoder().decode(request.user.contact_info)['data']

    keys = []

    data = []
    for info in contact_info:
        if privilege[str(info['info_id'])] == False:
            data.append(dict(info=info, enabled=False))
        else:
            data.append(dict(info=info, enabled=True))
        keys.append(str(info['info_id']))

    social_data = []
    socials = request.user.conns.all()
    for social in socials:
        if privilege[social.type+str(social.uid)] == False:
            social_data.append(dict(social=social, enabled=False))
        else:
            social_data.append(dict(social=social, enabled=True))
        keys.append(social.type+str(social.uid))

    if request.method == 'POST':
        p2 = {}
        for k in keys:
            if request.POST[k] == 'false':
                p2[k] = False
            else:
                p2[k] = True
        category.privilege = json.JSONEncoder().encode(p2)
        category.save()
        return redirect('/group/')
    else:
        return locals()
        # return render_to_response('group_setting.html', locals(), context_instance=RequestContext(request))

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
    relationship = Relationship.objects.filter(from_id=request.user)
    users = []
    for r in relationship:
        users.append(r.to_id)
    locations = []
    for user in users:
        locations += user.get_locations()
    return locals()

@render_to('find.html')
@login_required(login_url='/welcome/')
def find(request):
    guess = calc_friends(request.user)
    invites = request.user.invites.all()
    pendings = request.user.pendings.all()
    return locals()

@login_required(login_url='/welcome/')
def accept_invitation(request, pk):
    tou = request.user
    fromu = Profile.objects.get(pk=pk)
    inv = Invitation.objects.get(from_id=fromu, to_id=tou)
    if inv is not None:
        non_cat_from = fromu.cats.all()[0]
        non_cat_to = tou.cats.all()[0]
        Relationship.objects.create(from_id=fromu, to_id=tou, cat_id=non_cat_from)
        Relationship.objects.create(from_id=tou, to_id=fromu, cat_id=non_cat_to)
        inv.delete()
    return redirect('/find/')

@login_required(login_url='/welcome/')
def decline_invitation(request, pk):
    tou = request.user
    fromu = Profile.objects.get(pk=pk)
    inv = Invitation.objects.get(from_id=fromu, to_id=tou)
    if inv is not None:
        inv.delete()
    return redirect('/find/')

@login_required(login_url='/welcome/')
def add_invitation(request, pk):
    user = request.user
    to = Profile.objects.get(pk=pk)
    if len(Invitation.objects.filter(from_id=user, to_id=to)) == 0:
        if len(Invitation.objects.filter(from_id=to, to_id=user)) != 0:
            fromu = user
            tou = to
            non_cat_from = fromu.cats.all()[0]
            non_cat_to = tou.cats.all()[0]
            Relationship.objects.create(from_id=fromu, to_id=tou, cat_id=non_cat_from)
            Relationship.objects.create(from_id=tou, to_id=fromu, cat_id=non_cat_to)
        else:
            inv = Invitation.objects.create(from_id=user, to_id=to)
    return redirect('/find/')

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
