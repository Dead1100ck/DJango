from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .buisness_logic import *
from django.views import View
from CustomUser.models import CustomUser
from django.contrib.auth import logout, login

#Общая часть для всех пользователей - сотрудников и клиентов------------
def home_page(request):
	"""
		Домашная страница
	"""

	title = 'Домашняя страница'

	return render(request, 'base.html', {'title': title})


class LoginPage(View):
	"""
		Страница отвечающая за вход в аккаунт
	"""

	context = {
		'title': 'Вход',
	}
	
	def get(self, request):
		self.context['form'] = LoginForm()

		return render(request, 'base_login.html', self.context)

	def post(self, request):
		user = find_custom_user(request.POST['login'], request.POST['password'])

		if user:
			login(request, user.get())
			return HttpResponseRedirect('/account/')
		else:
			self.context['error'] = 'Введен не верный логин или пароль'

		return HttpResponseRedirect('/login/')


def user_logout(request):
	"""
		Выход пользователя из аккаунта
	"""

	logout(request)
	return HttpResponseRedirect('/')

def account_page(request):
	"""
		Страница аккаунта для сотрудников и клментов
	"""

	context = {
		'title': 'Профиль',
		'user': get_user(request.user)
	}

	if request.user.is_staff:
		return render(request, 'employee_pages/account.html', context)

	else:
		context['comments'] = get_user_comments(request.user)
		context['orders'] = get_client_orders(request.user)

		return render(request, 'user_pages/account.html', context)
#-----------------------------------------------------------------------

#Часть для пользователей не являющеющихся сотрудниками компании---------
class RegisterPage(View):
	"""
		Страница отвечающая за регистрацию, но только клиентов
		Сотрудников регистрирует администратор с помощью DJango admin
	"""

	context = {
		'title': 'Регистрация'
	}

	def get(self, request):
		if 'form' not in self.context:
			self.context['form'] = RegisterForm()

		return render(request, 'base_register.html', self.context)

	def post(self, request):
		form = RegisterForm(request.POST)
		errors = get_register_errors(request.POST)

		if len(errors) == 0:
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
		self.context['errors'] = errors
		return HttpResponseRedirect('/register/')


class AddComment(View):
	"""
		Добавление коментариев от пользователя
	"""

	def get(self, request):
		context = {
			'title': 'Оставить комментарий',
			'form': CommentForm()
		}

		return render(request, 'user_pages/add_comment_form.html', context)

	def post(self, request):
		add_comment(request.user, request.POST['title'], request.POST['description'])
		return HttpResponseRedirect('/account/')


def comments(request):
	"""
		Рендер страницы со всеми коментариями
	"""

	context = {
		'title': 'Комментарии',
		'comments': get_comments()
	}

	return render(request, 'base_comments.html', context)

class AddOrder(View):
	"""
		Добавление заказа от пользователя
	"""

	def get(self, request):
		context = {
			'title': 'Сделать заказ',
			'form': OrderForm()
		}

		return render(request, 'user_pages/add_order.html', context)

	def post(self, request):
		form = OrderForm(request.POST)

		if form.is_valid():
			add_order(request.user, form.cleaned_data['name'], form.cleaned_data['description'])

		return HttpResponseRedirect('/account/')

def confirm_order(request, id_order):
	set_order_status_work(id_order)
	return HttpResponseRedirect('/account/')

def delete_order(request, id_order):
	delete_user_order(id_order)
	return HttpResponseRedirect('/account/')

#-----------------------------------------------------------------------

#Часть для сотрудников компании-----------------------------------------
def orders_page(request):
	"""
	Страница с заказами для сотрудников
	"""

	context = {
		'title': 'Взять заказ'
	}
	user = get_user(request.user)

	if user.id_team == None:
		context['orders'] = get_orders()
		return render(request, 'employee_pages/orders.html', context)
	else:
		context['order'] = get_employee_order(request.user)
		return render(request, 'employee_pages/order.html', context)

def take_order(request, id_order):
	order = get_order(id_order)
	context = {
		'title': 'Взять заказ',
		'order': order
	}

	if get_team_order(id_order):
		create_team(request.user, id_order)
		return HttpResponseRedirect('/account/')

	if request.method == 'POST':
		set_order_status_confirm(id_order, request.POST['price'])
		print(request.POST)
		create_team(request.user, id_order)

		return HttpResponseRedirect('/account/')

	return render(request, 'employee_pages/take_order.html', context)

def complete_order(request, id_order):
	delete_team_and_complete_order(request.user, id_order)
	return HttpResponseRedirect('/account/')
#-----------------------------------------------------------------------