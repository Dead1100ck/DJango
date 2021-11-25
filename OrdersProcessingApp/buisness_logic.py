from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from CustomUser.models import CustomUser


def get_user(custom_user):
	if custom_user.is_staff:
		print(custom_user.id)
		user = Employee.objects.get(id_custom_user=custom_user.id)
		return user
	else:
		user = Client.objects.get(id_custom_user=custom_user.id)
		return user

#User--------------------------------------------------------------------------
def get_register_errors(post):
	errors = []

	if CustomUser.objects.filter(login=post['login']):
		errors.append('Такой логин уже зарегистрирован на сайте')
	if Client.objects.filter(email=post['email']) or Employee.objects.filter(email=post['email']):
		errors.append('Такой email уже используется')
	if Client.objects.filter(phone=post['phone']) or Employee.objects.filter(phone=post['phone']):
		errors.append('Такой телефон уже используется')
	if post['password1'] != post['password2']:
		errors.append('Пароли не совпадают')

	return errors

def register_user(login, password, first_name, second_name, email, phone):
	custom_user = CustomUser.objects.create(login=login, password=password)
	user = Client.objects.create(
		id_custom_user=custom_user,
		first_name=first_name,
		second_name=second_name,
		email=email,
		phone=phone)

def find_custom_user(login, password):
	return CustomUser.objects.filter(login=login, password=password)

def add_order(user, name, description):
	client = get_user(user)
	Order.objects.create(id_client=client, name=name, description=description)

def get_user_comments(custom_user):
	if custom_user.is_staff:
		return ''

	user = Client.objects.get(id_custom_user=custom_user.id)
	comments = Comment.objects.filter(id_client=user.id)

	if comments:
		return comments
	return ''

def get_comments():
	return Comment.objects.all()

def get_client_orders(custom_user):
	user = get_user(custom_user)
	orders = Order.objects.filter(id_client=user.id)

	if orders:
		return orders
	return ''

def add_comment(custom_user, title, description):
	user = Client.objects.get(id_custom_user=custom_user.id)

	Comment.objects.create(
		first_name=user.first_name,
		second_name=user.second_name,
		email=user.email,
		title=title,
		description=description,
		id_client=user
	)

def set_order_status_work(id_order):
	order = Order.objects.get(id=id_order)
	order.status = 'В работе'
	order.save()

def set_order_status_discard(id_order):
	order = Order.objects.get(id=id_order)
	order.status = 'В обработке'
	order.save()

def delete_user_order(id_order):
	order = Order.objects.get(id=id_order)
	
	if Team.objects.filter(id_order=id_order):
		team = Team.objects.get(id_order=id_order)
		employees = Employee.objects.filter(id_team=team.id)

		for employee in employees:
			employee.id_team = None
			employee.save()

	order.delete()

#Employee----------------------------------------------------------------------
def get_orders():
	return Order.objects.all()

def get_order(id_order):
	return Order.objects.get(id=id_order)

def get_team_order(id_order):
	if Team.objects.filter(id_order=id_order):
		return True
	else:
		return False

def get_employee_order(custom_user):
	user = get_user(custom_user)
	team = user.id_team
	return Order.objects.get(id=team.id_order.id)

def create_team(custom_user, id_order):
	user = get_user(custom_user)
	order = Order.objects.get(id=id_order)

	if len(Team.objects.filter(id_order=id_order)) == 0:
		Team.objects.create(id_order=order, name=order.name)
	
	user.id_team = Team.objects.get(id_order=id_order)
	user.save()

def get_employees_in_one_team(custom_user):
	user = get_user(custom_user)
	emlpoyees = Employee.objects.filter(id_team=user.id_team).exclude(email=user.email)
	return emlpoyees

def set_order_status_confirm(id_order, price):
	order = get_order(id_order)

	if order.status == 'В обработке':
		order.status = 'Ждет подтверждения'
		order.price = price
		order.save()

def delete_team_and_complete_order(custom_user, id_order):
	user = get_user(custom_user)
	team = user.id_team
	user.id_team = None
	user.save()

	if len(Employee.objects.filter(id_team=team)) == 0:
		team = Team.objects.get(id=team.id)
		team.delete()
		order = get_order(id_order)
		order.status = 'Завершен'
		print(order.status)
		order.save()