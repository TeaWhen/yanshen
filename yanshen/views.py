from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext

def home(request):
	pass

def profile(request):
	pass

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

def robots(reuqest):
	return render_to_response('robots.txt', locals(), context_instance=RequestContext(request))

def orca(request):
    return HttpResponse("b5da7f1e4f9066c4")
