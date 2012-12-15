# coding=utf8

from conns.models import AuthInfo
from users.models import Profile, Relationship
from conns.api_keys import *

from django.shortcuts import redirect

import requests
import urlparse
import urllib
import json


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
    return redirect("/me")


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
        nai.uname = user_info['name']
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
