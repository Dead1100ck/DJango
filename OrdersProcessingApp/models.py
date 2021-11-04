from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Client(models.Model):
	second_name = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30)
	middle_name = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	phone = models.CharField(max_length=11, unique=True)
	login = models.CharField(max_length=30)
	password = models.CharField(max_length=30)

	def __str__(self):
		return self.email + " " + self.phone


class Comment(models.Model):
	second_name = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30)
	middle_name = models.CharField(max_length=30)
	title = models.CharField(max_length=30, blank=True)
	description = models.TextField()
	email = models.CharField(max_length=30)
	id_client = models.ForeignKey(Client, on_delete=models.CASCADE)

	def __str__(self):
		return self.email + " " + self.title


class Contract(models.Model):
	task = models.TextField()
	name_of_project = models.CharField(max_length=30)
	id_client = models.ForeignKey(Client, on_delete=models.CASCADE)

	def __str__(self):
		return self.name_of_project


class Team(models.Model):
	id_contract = models.ForeignKey(Contract, on_delete=models.CASCADE)


class Project(models.Model):
	name_of_project = models.CharField(max_length=30)
	description = models.TextField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	id_team = models.ForeignKey(Team, on_delete=models.CASCADE)

	def __str__(self):
		return self.name_of_project + " " + str(self.price)


class Employee(models.Model):
	second_name = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30)
	middle_name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	email = models.CharField(max_length=30)
	login = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	status = models.IntegerField(validators=[
        MaxValueValidator(3),
        MinValueValidator(0)
    ])
	id_team = models.ForeignKey(Team, on_delete=models.CASCADE)

	def __str__(self):
		return self.second_name + " " + self.first_name + " " + self.middle_name