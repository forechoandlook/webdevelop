from django.shortcuts import render, reverse,redirect
from django.http import HttpResponse, HttpResponseRedirect

def index(requset):
	response = redirect('/home/')
	return response
	#return render(requset,"index.html")
