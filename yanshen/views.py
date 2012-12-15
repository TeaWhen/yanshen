from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext
from datetime import datetime

def index(request):
	time = datetime.now()
	hour = time.hour
	minute = time.minute
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def contact(request):
	time = datetime.now()
	hour = time.hour
	minute = time.minute
	return render_to_response('contact.html', locals(), context_instance=RequestContext(request))

def me(request):
	time = datetime.now()
	hour = time.hour
	minute = time.minute
	return render_to_response('me.html', locals(), context_instance=RequestContext(request))

def group(request):
	time = datetime.now()
	hour = time.hour
	minute = time.minute
	return render_to_response('group.html', locals(), context_instance=RequestContext(request))

def map(request):
	time = datetime.now()
	hour = time.hour
	minute = time.minute
	return render_to_response('map.html', locals(), context_instance=RequestContext(request))

def signup(request):
	time = datetime.now()
	hour = time.hour
	minute = time.minute
	if request.method == "POST":
		pass
	else:
		pass

def signin(request):
	time = datetime.now()
	hour = time.hour
	minute = time.minute
	if request.method == "POST":
		pass
	else:
		pass

def robots(request):
	return render_to_response('robots.txt', locals(), context_instance=RequestContext(request))

def humans(request):
	return render_to_response('humans.txt', locals(), context_instance=RequestContext(request))

def orca(request):
    return HttpResponse("b5da7f1e4f9066c4")
