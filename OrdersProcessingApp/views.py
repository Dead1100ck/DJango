from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *

# Create your views here.
def home(request):
	title = 'Домашняя страница'

	return render(request, 'base.html', {'title': title})

def register(request):
	title = 'Регистрация'

	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
			return HttpResponseRedirect('/login')
	else:
		form = RegisterForm()

	return render(request, 'base_register.html', {'title': title, 'form': form})

def login(request):
	title = 'Вход в аккаунт'

	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			return HttpResponseRedirect('/account')
	else:
		form = LoginForm()

	return render(request, 'base_login.html', {'title': title, 'form': form})

def account(request):
	return HttpResponse('account')