from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'yanshen.views.index'),
    url(r'^welcome/$', 'yanshen.views.welcome'),
    url(r'^index/$', 'yanshen.views.index'),
    url(r'^me/$', 'yanshen.views.me'),
    url(r'^contact/(\d+)/$', 'yanshen.views.contact'),
    url(r'^group/$', 'yanshen.views.group'),
    url(r'^group/(\d+)/$', 'yanshen.views.group_settings'),
    url(r'^category/(\d+)/$', 'yanshen.views.group_detail'),
    url(r'^map/$', 'yanshen.views.map'),
    url(r'^logout/$', 'yanshen.views.signout'),
    url(r'^find/$', 'yanshen.views.find'),
    url(r'^invitation/accept/(\d+)/$', 'yanshen.views.accept_invitation'),
    url(r'^invitation/decline/(\d+)/$', 'yanshen.views.decline_invitation'),
    url(r'^invitation/add/(\d+)/$', 'yanshen.views.add_invitation'),
    url(r'^robots.txt$', 'yanshen.views.robots'),
    url(r'^humans.txt$', 'yanshen.views.humans'),
    # url(r'^yanshen/', include('yanshen.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # for orca
    url(r'^orca.txt$', 'yanshen.views.orca'),
    url(r'^conns/', include('conns.urls')),
)

handler404 = 'yanshen.views.page_not_found'
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
