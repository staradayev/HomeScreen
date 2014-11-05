from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

def IndexView(request):
	template = loader.get_template('ato/index.html')
	context = RequestContext(request,)
	return HttpResponse(template.render(context))
