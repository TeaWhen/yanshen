# coding=utf8

from conns.models import AuthInfo
from users.models import Profile, Relationship
from conns.api_keys import *

from django.shortcuts import redirect

import requests
import urlparse
import json

 
def weibo_connect(request):
    args = {
        'response_type': "code",
        'client_id': WEIBO_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/weibo_callback"
    }
    return redirect(requests.get(WEIBO_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def weibo_callback(request):
    if "error" in request.args:
        errors = request.args
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': WEIBO_CLIENT_ID,
            'client_secret': WEIBO_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/weibo_callback",
            'code': request.args["code"]
        }
        r = requests.post(WEIBO_TOKEN_URL, params=args)
        auth_info = r.json
        nai = AuthInfo(type="weibo")
        nai.uid = auth_info['uid']
        nai.owner = request.user
        nai.tokens = r.text
        nai.save()
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
    if "error" in request.args:
        errors = request.args
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': RENREN_CLIENT_ID,
            'client_secret': RENREN_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/renren_callback",
            'code': request.args["code"]
        }
        r = requests.post(RENREN_TOKEN_URL, params=args)
        auth_info = r.json
        nai = AuthInfo(type="renren")
        nai.uid = auth_info['user']['id']
        nai.owner = request.user
        nai.tokens = r.text
        nai.save()
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
    if "error" in request.args:
        errors = request.args
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': GITHUB_CLIENT_ID,
            'client_secret': GITHUB_CLIENT_SECRET,
            'code': request.args["code"]
        }
        r = requests.post(GITHUB_TOKEN_URL, params=args)
        auth_info = urlparse.parse_qs(r.text)
        nai = AuthInfo(type="github")
        user_info = requests.get(GITHUB_API_ROOT+"/user", params={'access_token': auth_info['access_token'][0]}).json
        nai.uid = auth_info[user_info['id']]
        nai.owner = request.user
        nai.tokens = json.JSONEncoder().encode({'access_token': auth_info['access_token'][0]})
        nai.save()
    return redirect("/me")


def facebook_connect(request):
    args = {
        'client_id': FACEBOOK_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/facebook_callback",
        'scope': 'user_status,read_friendlists'
    }
    return redirect(requests.get(FACEBOOK_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def facebook_callback(request):
    if "error" in request.args:
        errors = request.args
    else:
        args = {
            'client_id': FACEBOOK_CLIENT_ID,
            'client_secret': FACEBOOK_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/facebook_callback",
            'code': request.args["code"]
        }
        r = requests.post(FACEBOOK_TOKEN_URL, params=args)
        auth_info = urlparse.parse_qs(r.text)
        nai = AuthInfo(type="facebook")
        user_info = requests.get(FACEBOOK_API_ROOT+"/me", params={'access_token': auth_info['access_token'][0], 'fields': 'id'}).json
        nai.uid = user_info['id']
        nai.owner = requests.user
        nai.tokens = json.JSONEncoder().encode({'access_token': auth_info['access_token'][0]})
        nai.save()
    return redirect("/me")

def facebook_friends(request, ai_id):
    ai = AuthInfo.objects.get(pk=ai_id)
    return

def tqq_connect(request):
    args = {
        'response_type': "code",
        'client_id': TQQ_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/tqq_callback",
    }
    return redirect(requests.get(TQQ_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def tqq_callback(request):
    if "error" in request.args:
        errors = request.args
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': TQQ_CLIENT_ID,
            'client_secret': TQQ_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/tqq_callback",
            'code': request.args["code"]
        }
        auth_info = urlparse.parse_qs(requests.post(TQQ_TOKEN_URL, params=args).text)
    return


def jiepang_connect(request):
    args = {
        'response_type': "code",
        'client_id': JIEPANG_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/jiepang_callback"
    }
    return redirect(requests.get(JIEPANG_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def jiepang_callback(request):
    if "error" in request.args:
        errors = request.args
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': JIEPANG_CLIENT_ID,
            'client_secret': JIEPANG_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/jiepang_callback",
            'code': request.args["code"]
        }
        auth_info = requests.post(JIEPANG_TOKEN_URL, params=args).json
    return

# twitter(oauth1...)
# def douban_connect():
#     args = {
#         'response_type': "code",
#         'client_id': DOUBAN_CLIENT_ID,
#         'redirect_uri': ROOT_URL+"conns/douban_callback",
#         'scope': "douban_basic_common,shuo_basic_r"
#     }
#     return redirect(requests.get(DOUBAN_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

# def douban_callback():
#     if "error" in request.args:
#         errors = request.args
#     else:
#         args = {
#             'grant_type': "authorization_code",
#             'client_id': DOUBAN_CLIENT_ID,
#             'client_secret': DOUBAN_CLIENT_SECRET,
#             'redirect_uri': ROOT_URL+"conns/douban_callback",
#             'code': request.args["code"]
#         }
#         auth_info = requests.post(DOUBAN_TOKEN_URL, params=args).json
#     return