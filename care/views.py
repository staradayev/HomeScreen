from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from care.models import Picture
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render

def logout(request, redirect_url=None):
	auth.logout(request)
	return HttpResponseRedirect('/care/loggedout')

def loggedout(request):
	template = loader.get_template('care/loggedout.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def email_check(user):
	if hasattr(user, 'email') and '@mail.ru' in user.email:
		return True
	else:
		return False

@user_passes_test(email_check)
def logged(request):
	return HttpResponse("You are logged user")

@user_passes_test(email_check)
def DetailView(request):
	picture_list = Picture.objects.order_by('-date_pub').all()
	paginator = Paginator(picture_list, 4)

	page = request.GET.get('page')
	try:
		pictures = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		pictures = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		pictures = paginator.page(paginator.num_pages)

	template = loader.get_template('care/detail.html')
	context = RequestContext(request, {
		'picture_list': pictures,
	})
	return HttpResponse(template.render(context))

class UserInfoForm(forms.Form):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)

@user_passes_test(email_check)
def InfoView(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserInfoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
			user = User.objects.get(username = request.user.username)
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.email = form.cleaned_data['email']
			user.save()
            # redirect to a new URL:
			return HttpResponseRedirect('/care/detail')

    # if a GET (or any other method) we'll create a blank form
    else:
    	user = User.objects.get(username = request.user.username)
        form = UserInfoForm(initial={
        	'first_name': user.first_name,
        	'last_name': user.last_name,
        	'email' : user.email})

    return render(request, 'care/myinfo.html', {'form': form})



