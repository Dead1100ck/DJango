from django.db import models
from django.conf import settings


class Client(models.Model):
	id_custom_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=30)
	email = models.CharField(max_length=30, unique=True)
	phone = models.CharField(max_length=11, unique=True)
	
	def __str__(self):
		return self.email + " " + self.phone


class Comment(models.Model):
	first_name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=30)
	title = models.CharField(max_length=30)
	description = models.TextField()
	email = models.CharField(max_length=30)
	id_client = models.ForeignKey(Client, on_delete=models.CASCADE)

	def __str__(self):
		return self.email + " " + self.title


class Order(models.Model):
	statuses = [('В обработке', 'В обработке'), ('Ждет подтверждения', 'Ждет подтверждения'), ('В работе', 'В работе'), ('Завершен', 'Завершен')]

	name = models.CharField(max_length=30)
	description = models.TextField()
	price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
	status = models.CharField(max_length=18, choices=statuses, default="В обработке")
	id_client = models.ForeignKey(Client, on_delete=models.CASCADE)

	def __str__(self):
		return "Заказ: " + self.name


class Team(models.Model):
	name = models.CharField(max_length=40)
	id_order = models.ForeignKey(Order, on_delete=models.CASCADE)

	def __str__(self):
		return "Команда: " + self.name


class Employee(models.Model):
	id_custom_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	email = models.CharField(max_length=30, unique=True)
	phone = models.CharField(max_length=11, unique=True)
	id_team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.first_name + ' ' + self.second_name 