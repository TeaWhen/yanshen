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
    args = {'client_id': RENREN_CLIENT_ID, 'redirect_uri': '127.0.0.1/conns/renren_callback','scope': 'read_user_status send_message'}
    return redirect(requests.get(RENREN_AUTH_URL, params=args).url)


def renren_callback():
    if "error" in request.args:
        error = request.args["error"]
        error_descrip = request.args["error_description"]
    else:
        code = request.args["code"]
    return


def github_connect():
    return


def github_callback():
    return

# douban, twitter, facebook, weixin, G+, github
