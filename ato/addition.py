from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.db.models import Sum
from care.models import Download, UserProfile, Picture, Organization

class HomeView:
	def __init__(self, request=False):
		self.request = request

	def IndexFile(s):
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
		context = RequestContext(self.request, {
			'downloads': downloads,
			'photographers': photographers,
			'pictures': pictures,
			'donated': donated,
			'organizations': organizations,
			'LANG': self.request.LANGUAGE_CODE,
		})
		return HttpResponse(template.render(context))