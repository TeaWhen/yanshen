# coding=utf8

from django.conf.urls import patterns, url

from conns import views

urlpatterns = patterns('',
    url(r'^weibo_connect$', views.weibo_connect, name='weibo_connect'),
    url(r'^weibo_callback$', views.weibo_connect, name='weibo_callback'),
    url(r'^renren_connect$', views.weibo_connect, name='renren_connect'),
    url(r'^renren_callback$', views.weibo_connect, name='renren_callback'),
    url(r'^github_connect$', views.weibo_connect, name='github_connect'),
    url(r'^github_callback$', views.weibo_connect, name='github_callback'),
    url(r'^facebook_connect$', views.weibo_connect, name='facebook_connect'),
    url(r'^facebook_callback$', views.weibo_connect, name='facebook_callback'),
    url(r'^tqq_connect$', views.weibo_connect, name='tqq_connect'),
    url(r'^tqq_callback$', views.weibo_connect, name='tqq_callback'),
    url(r'^jiepang_connect$', views.weibo_connect, name='jiepang_connect'),
    url(r'^jiepang_callback$', views.weibo_connect, name='jiepang_callback'),
)