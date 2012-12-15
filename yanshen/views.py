from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext

def index(request):
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def contact(request):
	return render_to_response('contact.html', locals(), context_instance=RequestContext(request))

def me(request):
	return render_to_response('me.html', locals(), context_instance=RequestContext(request))

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
	return render_to_response('robots.txt', locals(), context_instance=RequestContext(request))

def orca(request):
    return HttpResponse("b5da7f1e4f9066c4")
