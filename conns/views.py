# coding=utf8

from conns.models import AuthInfo
from users.models import Profile, Relationship
from conns.auth_settings import *

from django.shortcuts import redirect

from annoying.decorators import render_to

import requests


def weibo_connect():
    return redirect()


def weibo_callback():
    return


def renren_connect():
    args = {'client_id': RENREN_API_KEY, 'redirect_uri': '127.0.0.1/conns/','scope': 'read_user_status send_message'}
    return redirect(requests.get(RENREN_AUTH_URL, params=args).url)


def renren_callback():
    return


def github_connect():
    return


def github_callback():
    return

# douban, twitter, facebook, weixin, G+, github
