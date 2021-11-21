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


#Часть для пользователей не являющеющихся сотрудниками компании----------------
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
		user = find_custom_user(request.POST['login'], request.POST['password'])
		
		if user:
			login(request, user.get())
			return HttpResponseRedirect('/account/')

		return HttpResponseRedirect('/login/')


def user_logout(request):
	"""
		Выход пользователя из аккаунта
	"""

	logout(request)
	return HttpResponseRedirect('/')

def account_page(request):
	context = {
		'title': 'Профиль',
		'user': get_user(request.user)
	}

	if request.user.is_staff:
		context['project'] = get_project(request.user)

		return render(request, 'employee_pages/account.html', context)

	else:
		context['comments'] = get_user_comments(request.user)
		context['orders'] = get_user_orders(request.user)

		return render(request, 'user_pages/account.html', context)


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
#------------------------------------------------------------------------------

#Часть для сотрудников компании------------------------------------------------
"""
	take_order() 		- update status - work
	complete_order() 	- update status - complete
	employee_account()
	employee_complete_orders()
"""
def orders_page(request):
	context = {
		'title': 'Взять заказ'
	}
	user = get_user(request.user)

	if user['id_team'] is None:
		context['orders'] = get_orders()
		return render(request, 'employee_pages/orders.html', context)
	else:
		employees = get_employees_in_one_team(request.user)

		if employees and len(employees) > 1:
			context['employees'] = employees
		else:
			context['employees'] = False

		context['order'] = get_employee_order(request.user)
		return render(request, 'employee_pages/order.html', context)


def take_order(request, id_order):
	create_team_and_project(request.user, id_order)
	return HttpResponseRedirect('/account/')

#------------------------------------------------------------------------------