# coding=utf8

from conns.models import AuthInfo
from users.models import Profile, Relationship
from conns.api_keys import *

from django.shortcuts import redirect

from annoying.decorators import render_to

import requests
import urlparse

 
def weibo_connect():
    args = {
        'response_type': "code",
        'client_id': WEIBO_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/weibo_callback"
    }
    return redirect(requests.get(WEIBO_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def weibo_callback():
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
        auth_info = requests.post(WEIBO_TOKEN_URL, params=args).json
    return


def renren_connect():
    args = {
        'response_type': "code",
        'client_id': RENREN_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/renren_callback",
        'scope': 'read_user_status send_message'
    }
    return redirect(requests.get(RENREN_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def renren_callback():
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
        auth_info = requests.post(RENREN_TOKEN_URL, params=args).json
    return


def github_connect():
    args = {
        'response_type': "code",
        'client_id': GITHUB_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/github_callback",
        'scope': 'user'
    }
    return redirect(requests.get(GITHUB_AUTH_URL, param=args, prefetch=False, allow_redirects=False).url)

def github_callback():
    if "error" in request.args:
        errors = request.args
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': GITHUB_CLIENT_ID,
            'client_secret': GITHUB_CLIENT_SECRET,
            'code': request.args["code"]
        }
        auth_info = urlparse.parse_qs(requests.post(GITHUB_TOKEN_URL, params=args).text)
    return


def douban_connect():
    args = {
        'response_type': "code",
        'client_id': DOUBAN_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/douban_callback",
        'scope': "douban_basic_common,shuo_basic_r"
    }
    return redirect(requests.get(DOUBAN_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def douban_callback():
    if "error" in request.args:
        errors = request.args
    else:
        args = {
            'grant_type': "authorization_code",
            'client_id': DOUBAN_CLIENT_ID,
            'client_secret': DOUBAN_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/douban_callback",
            'code': request.args["code"]
        }
        auth_info = requests.post(DOUBAN_TOKEN_URL, params=args).json
    return


def facebook_connect():
    args = {
        'client_id': FACEBOOK_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/facebook_callback"
    }
    return redirect(requests.get(FACEBOOK_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def facebook_callback():
    if "error" in request.args:
        errors = request.args
    else:
        args = {
            'client_id': FACEBOOK_CLIENT_ID,
            'client_secret': FACEBOOK_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/facebook_callback",
            'code': request.args["code"]
        }
        auth_info = urlparse.parse_qs(requests.post(FACEBOOK_TOKEN_URL, params=args).text)
    return


def tqq_connect():
    args = {
        'response_type': "code",
        'client_id': TQQ_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/tqq_callback",
    }
    return redirect(requests.get(TQQ_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def tqq_callback():
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


def jiepang_connect():
    args = {
        'response_type': "code",
        'client_id': JIEPANG_CLIENT_ID,
        'redirect_uri': ROOT_URL+"conns/jiepang_callback"
    }
    return redirect(requests.get(JIEPANG_AUTH_URL, params=args, prefetch=False, allow_redirects=False).url)

def jiepang_callback():
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
    
# twitter, G+
