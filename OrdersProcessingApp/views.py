from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .buisness_logic import *
from django.views import View
from CustomUser.models import CustomUser
from django.contrib.auth import authenticate, logout, login

# Create your views here.
def home_page(request):
	title = 'Домашняя страница'

	return render(request, 'base.html', {'title': title})


class RegisterPage(View):
	"""
		Страница отвечающая за регистрацию, но только клиентов
		Сотрудников регистрирует администратор с помощью DJango admin
	"""

	context = {
		'title': 'Регистрация',
	}

	def get(self, request):
		if 'form' not in self.context:
			self.context['form'] = RegisterForm()

		return render(request, 'base_register.html', self.context)

	def post(self, request):
		form = RegisterForm(request.POST)
		
		if form.is_valid():
			form = RegisterForm()
			register_user(
				request.POST['login'],
				request.POST['password1'],
				request.POST['first_name'],
				request.POST['second_name'],
				request.POST['email'],
				request.POST['phone'])

			return HttpResponseRedirect('/login/')

		self.context['form'] = form
		return HttpResponseRedirect('/register/')


class LoginPage(View):
	"""
		Страница отвечающая за вход в аккаунт клиентов и сотрудников
	"""

	context = {
		'title': 'Вход',
	}
	
	def get(self, request):
		self.context['form'] = LoginForm()

		return render(request, 'base_login.html', self.context)

	def post(self, request):
		user = find_user(request.POST['login'], request.POST['password'])
		
		if user:
			login(request, user.get())
			return HttpResponseRedirect('/')

		return HttpResponseRedirect('/login/')


def user_logout(request):
	"""
		Выход пользователя из аккаунта
	"""

	logout(request)
	return HttpResponseRedirect('/')


def comments(request):
	return HttpResponse('Comments')

def contacts(request):
	return HttpResponse('Contacts')

def account_page(request):
	context = {
		'title': 'Профиль',
		'user': get_user(request.user),
		'comments': get_user_comments(request.user),
		'contracts': get_user_contracts(request.user)
	}

	if request.user.is_staff == False:
		return render(request, 'user_pages/account.html', context)

	return HttpResponse('Employee')