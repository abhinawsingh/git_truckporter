from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required	
import json as simplejson 
from django.views.decorators.cache import cache_control
from django.shortcuts import render
from UserAuth.models import *
import smtplib
import datetime

from django.views.decorators.csrf import csrf_exempt


def homepage(request):
	# if request.user is not None and request.user != AnonymousUser():
	# 	user = User.objects.filter(username = request.user)
	# 	name = user.values('first_name')[0]['first_name'] + " " + user.values('last_name')[0]['last_name'][0:1]
	# 	return render(request, 'dashboard.html',{'login_name':name})
	# user = CustomUser.objects.create_user("Sourabh", first_name="Sourabh",last_name = "Edake", email = "sdnedake@gmail.com",password="sourabh" ,mobile = "9981882123", dob =  "2015/12/12",  gender = "M")
	# user.save()
	return  render(request, 'homepage.html')

def forgot_password(request):
	return render(request, 'forgot_password.html')

def logout_start(request):
	logout(request)
	request.session.flush()
	if hasattr(request, 'user'):
 		request.user = AnonymousUser()
	return HttpResponseRedirect('/')

def reset_password(request):
	#RESET USER PASSWORD
	#INPUT ARGUMENTS: username, email
	username 	= request.POST.get("username")
	email 		= request.POST.get("email")
	user_exists	= CustomUser.objects.filter(username = username, email = email)
	if(len(user_exists)>0):
		#CREDENTIALS ARE TRUE, SEND THE EMAIL
		#AND REDIRECT TO THE HOMEPAGE WITH THE POSITIVE MESSAGE
		sender = 'truckporter.2016@gmail.com'
		receivers = [email]
		message = "This is a test e-mail message."

		try:
			mail_server = smtplib.SMTP('smtp.gmail.com', 587)
			mail_server.ehlo()
			mail_server.starttls()
			mail_server.login('truckporter.2016@gmail.com', 'truckporterDefault@101')
			mail_server.sendmail(sender, receivers, message)			
			return render(request, 'homepage.html',
								{	'msg_type':'success',
									'msg_title' : 'Email sent successfully',
									'msg_text':	"An email has been sent to your registered email " + email + 
									" with instructions to reset your password."})

		except Exception as e:
			return render(request, 'forgot_password.html', 
								{	'msg_type':'error',
									'msg_title' : 'Could not recover your password now',
									'msg_text':	"Unable to request to recover your password now. Please try again later."})

	#ON INVALID CREDENTIALS REDIRECT AGAIN TO forgot_password PAGE
	return render(request, 'forgot_password.html',
						{	'msg_type':'error',
							'msg_title' : 'Invalid Input',
							'msg_text':	"Wrong username or email was provided!"})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_dashboard(request):
	name = request.session['name']
	return render(request,"dashboard.html",{'login_name': name})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_referrals(request):
	name = request.session['name']
	return render(request,"referrals.html",{'login_name':name})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_profile(request):
	name = request.session['name']
	user_exists	= CustomUser.objects.filter(username = request.user)
	email = user_exists.values('email')[0]['email']
	full_name = user_exists.values('first_name')[0]['first_name'] + " " + user_exists.values('last_name')[0]['last_name']
	mobile = user_exists.values('mobile')[0]['mobile']
	gender = user_exists.values('gender')[0]['gender']
	dob = user_exists.values('dob')[0]['dob']
	return render(request,"my_profile.html",{'login_name':name, 'email':email, 'full_name':full_name, 'mobile':mobile, 'gender' :gender, 'dob':dob})

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_start(request):
	# if request.user is not None and request.user != AnonymousUser():
	# 	user = User.objects.filter(username = request.user)
	# 	name = user.values('first_name')[0]['first_name'] + " " + user.values('last_name')[0]['last_name'][0:1]
	# 	if(len(name)<3): name="User"
	# 	return render(request, 'dashboard.html',{'login_name':name})
	#REQUESTING LOGIN FIRST

	request.session.flush()
	if hasattr(request, 'user'):
 		request.user = AnonymousUser()
	username 	= request.POST.get("username")
	password	= request.POST.get("password")
	# remember	= request.POST.get("remember")	

	user=authenticate(username=username,password=password)

	if user is not None:
		# if remember is not None:
		# 	request.session.set_expiry(0)
		if user.is_active:
			login(request, user)
		
		user = CustomUser.objects.filter(username = request.user)
		name = user.values('first_name')[0]['first_name'] + " " + user.values('last_name')[0]['last_name'][0:1]
		if(len(name)<3): name="User"
		request.session['name'] = name
		return show_dashboard(request)


	return render(request, 'homepage.html',
						{	'msg_type':'error',
							'msg_title' : 'Invalid Input',
							'msg_text':	"Wrong username or email was provided!"})

def ajax_change_password(request):
	name = request.session['name']
	user	= CustomUser.objects.filter(username = request.user)
	username = user.values('username')[0]['username']

	old_p = request.GET.get('old_password')
	new_p = request.GET.get('new_password')
	verify = authenticate(username= username, password=old_p)
	if verify is None:
		data = {"text":"You entered a Wrong password.", "status": "error"}
		return HttpResponse(simplejson.dumps(data))
	else:
		new_user	= CustomUser.objects.get(username = request.user)
		new_user.set_password(new_p);
		new_user.save()
		verify = authenticate(username= username, password=new_p)
		logout(request)
		login(request,verify)
		name = user.values('first_name')[0]['first_name'] + " " + user.values('last_name')[0]['last_name'][0:1]
		if(len(name)<3): name="User"
		request.session['name'] = name
		data = {"text":"Password updated.", "status": "success"}
		return HttpResponse(simplejson.dumps(data))

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_about_us(request):
	name = request.session['name']
	return render(request,"about_us.html",{'login_name':name})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_contact_us(request):
	name = request.session['name']
	return render(request,"contact_us.html",{'login_name':name})

