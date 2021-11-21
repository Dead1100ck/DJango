from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from CustomUser.models import CustomUser


def get_user(custom_user):
	if custom_user.is_staff:
		user = Employee.objects.get(id_custom_user=custom_user.id)
		user_data = {
			'login': custom_user.login,
			'password': custom_user.password,
			'first_name': user.first_name,
			'second_name': user.second_name,
			'adress': user.address,
			'email': user.email,
			'phone': user.phone,
			'id_team': user.id_team
		}
	else:
		user = Client.objects.get(id_custom_user=custom_user.id)
		user_data = {
			'login': custom_user.login,
			'password': custom_user.password,
			'first_name': user.first_name,
			'second_name': user.second_name,
			'email': user.email,
			'phone': user.phone
		}

	return user_data

#User--------------------------------------------------------------------------
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

def get_user_comments(custom_user):
	if custom_user.is_staff:
		return ''

	user = Client.objects.get(id_custom_user=custom_user.id)
	comments = Comment.objects.filter(id_client=user.id)

	if comments:
		return comments
	return ''

def get_user_orders(custom_user):
	if custom_user.is_staff:
		return ''

	user = Client.objects.get(id_custom_user=custom_user.id)
	contract = Order.objects.filter(id_client=user.id)

	if contract:
		return contract
	return ''

def get_comments():
	return Comment.objects.all()

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

#Employee----------------------------------------------------------------------
def get_orders():
	return Order.objects.all()

def get_employee_order(custom_user):
	user = get_user(custom_user)
	team = user['id_team']
	return Order.objects.get(id=team.id_order.id)

def create_team_and_project(custom_user, id_order):
	if Team.objects.filter(id_order=id_order):
		team = Team.objects.filter(id_order=id_order).get()
	else:
		team = Team.objects.create(id_order=id_order)
		order = Order.objects.get(id=id_order)
		Project.objects.create(id_team=team, name_of_project=order.name_of_project, description=order.task, price=20000)

	user = Employee.objects.get(id_custom_user=custom_user.id)
	user.id_team = team
	user.save()

def get_employees_in_one_team(custom_user):
	user = get_user(custom_user)
	emlpoyees = Employee.objects.filter(id_team=user['id_team'].id).exclude(email=user['email'])
	return emlpoyees

def get_project(custom_user):
	user = get_user(custom_user)
	team = user['id_team']
	return Project.objects.get(id_team=team.id)