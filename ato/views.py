from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.db.models import Sum
from care.models import Download, UserProfile, Picture, Organization
from addition import HomeView
import re
from django.conf import settings


def IndexView(request):

	if request.LANGUAGE_CODE:
		return HttpResponseRedirect('/'+request.LANGUAGE_CODE)

def IndexUAView(request):
	downloads = Download.objects.all().count()
	photographers = UserProfile.objects.all().count()
	pictures = Picture.objects.filter(approve_status=True).count()
	amount = Download.objects.aggregate(Sum('amount'))
	if amount['amount__sum']:
		donated = str(int(amount['amount__sum']) * settings.DONATED_LEFT)
	else:
		donated = 0
	organizations = []

	orgs = Organization.objects.all()
	for org in orgs:
		organization = {};
		organization['name'] = org.name
		organization['description'] = org.description
		organizations.append(organization)

	is_mobile = False;

	if request.META.has_key('HTTP_USER_AGENT'):
		user_agent = request.META['HTTP_USER_AGENT']

		# Test common mobile values.
		pattern = "(up.browser|up.link|mmp|symbian|smartphone|midp|wap|phone|windows ce|pda|mobile|mini|palm|netfront)"
		prog = re.compile(pattern, re.IGNORECASE)
		match = prog.search(user_agent)

		if match:
			is_mobile = True;
		else:
			# Nokia like test for WAP browsers.
			# http://www.developershome.com/wap/xhtmlmp/xhtml_mp_tutorial.asp?page=mimeTypesFileExtension

			if request.META.has_key('HTTP_ACCEPT'):
				http_accept = request.META['HTTP_ACCEPT']

				pattern = "application/vnd\.wap\.xhtml\+xml"
				prog = re.compile(pattern, re.IGNORECASE)

				match = prog.search(http_accept)

				if match:
					is_mobile = True

		if not is_mobile:
			# Now we test the user_agent from a big list.
			user_agents_test = ("w3c ", "acs-", "alav", "alca", "amoi", "audi",
								"avan", "benq", "bird", "blac", "blaz", "brew",
								"cell", "cldc", "cmd-", "dang", "doco", "eric",
								"hipt", "inno", "ipaq", "java", "jigs", "kddi",
								"keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
								"maui", "maxo", "midp", "mits", "mmef", "mobi",
								"mot-", "moto", "mwbp", "nec-", "newt", "noki",
								"xda",  "palm", "pana", "pant", "phil", "play",
								"port", "prox", "qwap", "sage", "sams", "sany",
								"sch-", "sec-", "send", "seri", "sgh-", "shar",
								"sie-", "siem", "smal", "smar", "sony", "sph-",
								"symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
								"upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
								"wapi", "wapp", "wapr", "webc", "winw", "winw",
								"xda-",)

			test = user_agent[0:4].lower()
			if test in user_agents_test:
				is_mobile = True

	request.is_mobile = is_mobile

	if request.is_mobile:
		template = loader.get_template('ato/index-mobile.html')
	else:
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

def IndexENView(request):
	downloads = Download.objects.all().count()
	photographers = UserProfile.objects.all().count()
	pictures = Picture.objects.filter(approve_status=True).count()
	amount = Download.objects.aggregate(Sum('amount'))
	if amount['amount__sum']:
		donated = str(int(amount['amount__sum']) * settings.DONATED_LEFT)
	else:
		donated = 0
	organizations = []

	orgs = Organization.objects.all()
	for org in orgs:
		organization = {};
		organization['name'] = org.name
		organization['description'] = org.description
		organizations.append(organization)

	is_mobile = False;

	if request.META.has_key('HTTP_USER_AGENT'):
		user_agent = request.META['HTTP_USER_AGENT']

		# Test common mobile values.
		pattern = "(up.browser|up.link|mmp|symbian|smartphone|midp|wap|phone|windows ce|pda|mobile|mini|palm|netfront)"
		prog = re.compile(pattern, re.IGNORECASE)
		match = prog.search(user_agent)

		if match:
			is_mobile = True;
		else:
			# Nokia like test for WAP browsers.
			# http://www.developershome.com/wap/xhtmlmp/xhtml_mp_tutorial.asp?page=mimeTypesFileExtension

			if request.META.has_key('HTTP_ACCEPT'):
				http_accept = request.META['HTTP_ACCEPT']

				pattern = "application/vnd\.wap\.xhtml\+xml"
				prog = re.compile(pattern, re.IGNORECASE)

				match = prog.search(http_accept)

				if match:
					is_mobile = True

		if not is_mobile:
			# Now we test the user_agent from a big list.
			user_agents_test = ("w3c ", "acs-", "alav", "alca", "amoi", "audi",
								"avan", "benq", "bird", "blac", "blaz", "brew",
								"cell", "cldc", "cmd-", "dang", "doco", "eric",
								"hipt", "inno", "ipaq", "java", "jigs", "kddi",
								"keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
								"maui", "maxo", "midp", "mits", "mmef", "mobi",
								"mot-", "moto", "mwbp", "nec-", "newt", "noki",
								"xda",  "palm", "pana", "pant", "phil", "play",
								"port", "prox", "qwap", "sage", "sams", "sany",
								"sch-", "sec-", "send", "seri", "sgh-", "shar",
								"sie-", "siem", "smal", "smar", "sony", "sph-",
								"symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
								"upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
								"wapi", "wapp", "wapr", "webc", "winw", "winw",
								"xda-",)

			test = user_agent[0:4].lower()
			if test in user_agents_test:
				is_mobile = True

	request.is_mobile = is_mobile

	if request.is_mobile:
		template = loader.get_template('ato/index-mobile.html')
	else:
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

def SocialView(request):
	template = loader.get_template('ato/social.html')
	context = RequestContext(request, {'LANG': request.LANGUAGE_CODE})
	return HttpResponse(template.render(context))
