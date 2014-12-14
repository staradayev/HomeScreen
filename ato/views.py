from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Sum
from care.models import Download, UserProfile, Picture, Organization

def IndexView(request):
	downloads = Download.objects.all().count()
	photographers = UserProfile.objects.all().count()
	pictures = Picture.objects.filter(approve_status=True).count()
	amount = Download.objects.aggregate(Sum('amount'))
	if amount['amount__sum']:
		donated = amount['amount__sum']
	else:
		donated = 0
	organizations = []

	orgs = Organization.objects.all()
	for org in orgs:
		organization = {};
		organization['name'] = org.name
		organization['description'] = org.description
		organizations.append(organization)

	template = loader.get_template('ato/index.html')
	context = RequestContext(request, {
		'downloads': downloads,
		'photographers': photographers,
		'pictures': pictures,
		'donated': donated,
		'organizations': organizations,
		'LANG': request.LANGUAGE_CODE,
	})
	return HttpResponse(template.render(context))

def PPEView(request):
	template = loader.get_template('ato/ppEnglish.html')
	context = RequestContext(request, {'LANG': request.LANGUAGE_CODE})
	return HttpResponse(template.render(context))

def PPUView(request):
	template = loader.get_template('ato/ppUkrainian.html')
	context = RequestContext(request, {'LANG': request.LANGUAGE_CODE})
	return HttpResponse(template.render(context))
