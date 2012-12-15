from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response, RequestContext
import time

def index(request):
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def contact(request):
	return render_to_response('contact.html', locals(), context_instance=RequestContext(request))

def me(request):
	return render_to_response('me.html', locals(), context_instance=RequestContext(request))

def group(request):
	return render_to_response('group.html', locals(), context_instance=RequestContext(request))

def map(request):
	return render_to_response('map.html', locals(), context_instance=RequestContext(request))

def signup(request):
	if request.method == "POST":
		pass
	else:
		pass

def signin(request):
	if request.method == "POST":
		pass
	else:
		pass

def robots(request):
	return render(request, 'robots.txt', content_type="text/plain")

def humans(request):
	return render(request, 'humans.txt', content_type="text/plain")

def orca(request):
    return HttpResponse("b5da7f1e4f9066c4", content_type="text/plain")
