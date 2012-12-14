# coding=utf8

from conns.models import AuthInfo
from users.models import Profile, Relationship
from conns.auth_settings import *

from django.shortcuts import redirect

from annoying.decorators import render_to

import requests
import urlparse


def weibo_connect():
    return redirect()

def weibo_callback():
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
        return
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
    return

def github_callback():
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
        return
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
        return
    else:
        args = {
            'client_id': FACEBOOK_CLIENT_ID,
            'client_secret': FACEBOOK_CLIENT_SECRET,
            'redirect_uri': ROOT_URL+"conns/facebook_callback",
            'code': request.args["code"]
        }
        auth_info = urlparse.parse_qs(requests.post(FACEBOOK_TOKEN_URL, params=args).text)
    return

# twitter, weixin, G+, github
