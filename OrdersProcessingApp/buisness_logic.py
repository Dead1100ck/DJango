from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from CustomUser.models import CustomUser


def register_user(login, password, first_name, second_name, email, phone):
	custom_user = CustomUser.objects.create(login=login, password=password)
	user = Client.objects.create(
		id_custom_user=custom_user,
		first_name=first_name,
		second_name=second_name,
		email=email,
		phone=phone)

def find_user(login, password):
	return CustomUser.objects.filter(login=login, password=password)

def get_user(custom_user):
	user = Client.objects.get(id_custom_user=custom_user.id)

	return {
		'login': custom_user.login,
		'password': custom_user.password,
		'first_name': user.first_name,
		'second_name': user.second_name,
		'email': user.email,
		'phone': user.phone
	}

def get_user_comments(custom_user):
	user = Client.objects.get(id_custom_user=custom_user.id)
	comments = Comment.objects.filter(id_client=user.id)

	if comments:
		return comments
	return False

def get_user_contracts(custom_user):
	user = Client.objects.get(id_custom_user=custom_user.id)
	contract = Contract.objects.filter(id_client=user.id)

	if contract:
		return contract
	return False
