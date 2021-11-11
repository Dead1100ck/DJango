from django import forms
from .models import *

class RegisterForm(forms.Form):
	first_name = forms.CharField(label='Имя', max_length='30', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
	second_name = forms.CharField(label='Фамилия', max_length='30', widget=forms.TextInput(attrs={'placeholder': 'фамилия'}))
	email = forms.CharField(label='Email', max_length='30', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	tel = forms.CharField(label='Номер телефона', max_length='11', widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
	login = forms.CharField(label='Логин', max_length='30', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
	password1 = forms.CharField(label='Пароль', max_length='30', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Повторите пароль', max_length='30', widget=forms.PasswordInput())

	def clean_password2(self):
		cd = self.cleaned_data

		if cd['password1'] != cd['password2']:
			raise forms.ValidationError("Пароли не совпадают")


class LoginForm(forms.Form):
	login = forms.CharField(label='Логин', max_length='30', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
	password = forms.CharField(label='Пароль', max_length='30', widget=forms.PasswordInput())