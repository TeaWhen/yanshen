# coding=utf8

from conns.models import AuthInfo
from users.models import Profile, Relationship, Invitation
from conns.api_keys import *

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

import requests
import urlparse
import urllib
import json
import hashlib

@login_required(login_url='/welcome/')
def weibo_connect(request):
    args = {
        'response_type': "code",
        'client_id': WEIBO_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/weibo_callback"
    }
    return redirect(requests.get(WEIBO_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def weibo_callback(request):
    if "error" in request.GET:
        errors = request.GET
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': WEIBO_CLIENT_ID,
            'client_secret': WEIBO_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/weibo_callback",
            'code': request.GET["code"]
        }
        r = requests.post(WEIBO_TOKEN_URL, params=args)
        auth_info = r.json
        nowai = AuthInfo.objects.filter(uid=auth_info['uid'])
        if len(nowai):
            nai = nowai[0]
        else:
            nai = AuthInfo(type="weibo", owner=request.user)
            nai.uid = auth_info['uid']
        user_info = requests.get(WEIBO_API_ROOT+"/users/show.json", params={'access_token': auth_info['access_token'], 'uid': auth_info['uid']}).json
        nai.uname = user_info['screen_name']
        nai.icon = "icon-weibo"
        nai.url = "http://weibo.com/"+str(auth_info['uid'])
        nai.tokens = r.text
        nai.save()
        for c in request.user.cats.all().all():
            cp = json.JSONDecoder().decode(c.privilege)
            cp[nai.type+str(nai.uid)] = True
            c.privilege = json.JSONEncoder().encode(cp)
            c.save()
    return redirect("/me")

def weibo_friends(user):
    result = []
    all_weibos = AuthInfo.objects.filter(type="weibo")
    ais = user.conns.filter(type="weibo")
    for ai in ais:
        auth_info = json.JSONDecoder().decode(ai.tokens)
        r = requests.get(WEIBO_API_ROOT+"/friendships/friends/bilateral/ids.json", params={'access_token': auth_info['access_token'], 'uid': ai.uid, 'count': 200})
        ids = r.json['ids']
        for i in ids:
            for p in all_weibos:
                if str(i) == p.uid:
                    result.append(p.owner)
    return result


@login_required(login_url='/welcome/')
def renren_connect(request):
    args = {
        'response_type': "code",
        'client_id': RENREN_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/renren_callback",
        'scope': 'read_user_status send_message'
    }
    return redirect(requests.get(RENREN_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def renren_callback(request):
    if "error" in request.GET:
        errors = request.GET
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': RENREN_CLIENT_ID,
            'client_secret': RENREN_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/renren_callback",
            'code': request.GET["code"]
        }
        r = requests.post(RENREN_TOKEN_URL, params=args)
        auth_info = r.json
        nowai = AuthInfo.objects.filter(uid=auth_info['user']['id'])
        if len(nowai):
            nai = nowai[0]
        else:
            nai = AuthInfo(type="renren", owner=request.user)
            nai.uid = auth_info['user']['id']
        nai.uname = auth_info['user']['name']
        nai.icon = "icon-renren"
        nai.url = "http://renren.com/"+str(auth_info['user']['id'])
        nai.tokens = r.text
        nai.save()
        for c in request.user.cats.all():
            cp = json.JSONDecoder().decode(c.privilege)
            cp[nai.type+str(nai.uid)] = True
            c.privilege = json.JSONEncoder().encode(cp)
            c.save()
        u = request.user
        for a in auth_info['user']['avatar']:
            if a['type'] == 'main':
                aurl = a['url']
        u.avatar = aurl
        u.save()
    return redirect("/me")

def renren_friends(user):
    result = []
    all_renrens = AuthInfo.objects.filter(type="renren")
    ais = user.conns.filter(type="renren")
    for ai in ais:
        auth_info = json.JSONDecoder().decode(ai.tokens)
        args = {
            'v': "1.0",
            'access_token': auth_info['access_token'],
            'format': "json",
            'method': "friends.getFriends"
        }
        sig = ""
        y = []
        for xk in args.keys():
            y.append("{}={}".format(xk, args[xk]))

        y.sort()
        for xx in y:
            sig += xx

        sig += RENREN_CLIENT_SECRET
        args['sig'] = hashlib.md5(sig).hexdigest()
        r = requests.post(RENREN_API_ROOT, params=args)
        rj = r.json
        for z in rj:
            for p in all_renrens:
                if str(z['id']) == p.uid:
                    result.append(p.owner)
    return result


@login_required(login_url='/welcome/')
def github_connect(request):
    args = {
        'response_type': "code",
        'client_id': GITHUB_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/github_callback",
        'scope': 'user'
    }
    return redirect(requests.get(GITHUB_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def github_callback(request):
    if "error" in request.GET:
        errors = request.GET
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': GITHUB_CLIENT_ID,
            'client_secret': GITHUB_CLIENT_SECRET,
            'code': request.GET["code"]
        }
        r = requests.post(GITHUB_TOKEN_URL, params=args)
        auth_info = urlparse.parse_qs(r.text)
        user_info = requests.get(GITHUB_API_ROOT+"/user", params={'access_token': auth_info['access_token'][0]}).json
        nowai = AuthInfo.objects.filter(uid=user_info['id'])
        if len(nowai):
            nai = nowai[0]
        else:
            nai = AuthInfo(type="github", owner=request.user)
            nai.uid = user_info['id']
        if 'name' in user_info:
            nai.uname = user_info['name']
        else:
            nai.uname = user_info['login']
        nai.icon = "icon-github"
        nai.url = user_info['html_url']
        nai.tokens = r.text
        nai.save()
        for c in request.user.cats.all():
            cp = json.JSONDecoder().decode(c.privilege)
            cp[nai.type+str(nai.uid)] = True
            c.privilege = json.JSONEncoder().encode(cp)
            c.save()
    return redirect("/me")

def github_friends(user):
    return []

# def facebook_connect(request):
#     args = {
#         'client_id': FACEBOOK_CLIENT_ID,
#         'redirect_uri': ROOT_URL+"conns/facebook_callback",
#         'scope': 'user_status,read_friendlists'
#     }
#     rurl = "%s?%s" % (FACEBOOK_AUTH_URL, urllib.urlencode(args))
#     return redirect(rurl)

# def facebook_callback(request):
#     if "error" in request.GET:
#         errors = request.GET
#     else:
#         args = {
#             'client_id': FACEBOOK_CLIENT_ID,
#             'client_secret': FACEBOOK_CLIENT_SECRET,
#             'redirect_uri': ROOT_URL+"conns/facebook_callback",
#             'code': request.GET["code"]
#         }
#         r = requests.post(FACEBOOK_TOKEN_URL, params=args)
#         auth_info = urlparse.parse_qs(r.text)
#         nai = AuthInfo(type="facebook", owner=request.user)
#         user_info = requests.get(FACEBOOK_API_ROOT+"/me", params={'access_token': auth_info['access_token'][0], 'fields': 'id,name'}).json
#         nai.uid = user_info['id']
#         nai.uname = user_info['name']
#         nai.tokens = r.text
#         nai.save()
#     return redirect("/me")

# def facebook_friends(request, ai_id):
#     ai = AuthInfo.objects.get(pk=ai_id)
#     return


@login_required(login_url='/welcome/')
def tqq_connect(request):
    args = {
        'response_type': "code",
        'client_id': TQQ_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/tqq_callback",
    }
    return redirect(requests.get(TQQ_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def tqq_callback(request):
    if "error" in request.GET:
        errors = request.GET
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': TQQ_CLIENT_ID,
            'client_secret': TQQ_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/tqq_callback",
            'code': request.GET["code"]
        }
        r = requests.post(TQQ_TOKEN_URL, params=args)
        auth_info = urlparse.parse_qs(r.text)
        nowai = AuthInfo.objects.filter(uid=auth_info['name'][0])
        if len(nowai):
            nai = nowai[0]
        else:
            nai = AuthInfo(type="tqq", owner=request.user)
            nai.uid = auth_info['name'][0]
        common_args = {
            'oauth_consumer_key': TQQ_CLIENT_ID,
            'access_token': auth_info['access_token'][0],
            'openid': auth_info['openid'][0],
            'clientip': "42.121.18.11",
            'oauth_version': "2.a"
        }
        user_info = requests.get(TQQ_API_ROOT+"/user/info", params=common_args).json
        nai.uname = user_info['data']['nick']
        nai.icon = "icon-tenxunweibo"
        nai.url = "http://t.qq.com/"+str(auth_info['name'][0])
        nai.tokens = r.text
        nai.save()
        for c in request.user.cats.all():
            cp = json.JSONDecoder().decode(c.privilege)
            cp[nai.type+str(nai.uid)] = True
            c.privilege = json.JSONEncoder().encode(cp)
            c.save()
    return redirect("/me")

def tqq_friends(user):
    return []


@login_required(login_url='/welcome/')
def jiepang_connect(request):
    args = {
        'response_type': "code",
        'client_id': JIEPANG_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/jiepang_callback"
    }
    return redirect(requests.get(JIEPANG_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def jiepang_callback(request):
    if "error" in request.GET:
        errors = request.GET
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': JIEPANG_CLIENT_ID,
            'client_secret': JIEPANG_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/jiepang_callback",
            'code': request.GET["code"]
        }
        r = requests.post(JIEPANG_TOKEN_URL, params=args)
        auth_info = r.json
        user_info = requests.get(JIEPANG_API_ROOT+"/users/show", params={'source': JIEPANG_CLIENT_ID, 'access_token': auth_info['access_token']}).json
        nowai = AuthInfo.objects.filter(uid=user_info['id'])
        if len(nowai):
            nai = nowai[0]
        else:
            nai = AuthInfo(type="jiepang", owner=request.user) 
            nai.uid = user_info['id']
        nai.uname = user_info['nick']
        nai.icon = "icon-qicheren"
        nai.url = "http://jiepang.com/user/"+str(user_info['id'])
        nai.tokens = r.text
        nai.save()
        for c in request.user.cats.all():
            cp = json.JSONDecoder().decode(c.privilege)
            cp[nai.type+str(nai.uid)] = True
            c.privilege = json.JSONEncoder().encode(cp)
            c.save()
    return redirect("/me")

def jiepang_friends(user):
    return []


def calc_friends(user):
    friends = {}
    already = []
    af = Relationship.objects.filter(from_id=user)
    for aaf in af:
        already.append(aaf.to_id)
    af = Invitation.objects.filter(from_id=user)
    for aaf in af:
        already.append(aaf.to_id)
    af = Invitation.objects.filter(to_id=user)
    for aaf in af:
        already.append(aaf.from_id)
    ff = weibo_friends(user)
    for f in ff:
        if not f in already:
            friends[f.id] = {'user': f, 'icons': ["icon-weibo"]}
    ff = renren_friends(user)
    for f in ff:
        if not f in already:
            if f.id in friends:
                friends[f.id]['icons'].append("icon-renren")
            else:
                friends[f.id] = {'user': f, 'icons': ["icon-renren"]}
    ff = github_friends(user)
    for f in ff:
        if not f in already:
            if f.id in friends:
                friends[f.id]['icons'].append("icon-github")
            else:
                friends[f.id] = {'user': f, 'icons': ["icno-github"]}
    ff = tqq_friends(user)
    for f in ff:
        if not f in already:
            if f.id in friends:
                friends[f.id]['icons'].append("icno-tenxunweibo")
            else:
                friends[f.id] = {'user': f, 'icons': ["icon-tenxunweibo"]}
    ff = jiepang_friends(user)
    for f in ff:
        if not f in already:
            if f.id in friends:
                friends[f.id]['icons'].append("icon-qicheren")
            else:
                friends[f.id] = {'user': f, 'icons': ["icon-qicheren"]}
    return friends
