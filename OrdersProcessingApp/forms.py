from django import forms
from django.forms import ModelForm
from .models import *

class RegisterForm(forms.Form):
	first_name = forms.CharField(label='Имя', max_length='30', widget=forms.TextInput(attrs={'placeholder': 'Иван'}))
	second_name = forms.CharField(label='Фамилия', max_length='30', widget=forms.TextInput(attrs={'placeholder': 'Иванович'}))
	email = forms.CharField(label='Email', max_length='30', widget=forms.TextInput(attrs={'placeholder': 'forexmple@mail.ru'}))
	phone = forms.CharField(label='Номер телефона', max_length='11', widget=forms.TextInput(attrs={'placeholder': '79998887766'}))
	login = forms.CharField(label='Логин', max_length='30', widget=forms.TextInput(attrs={'placeholder': 'Придумайте логин'}))
	password1 = forms.CharField(label='Пароль', max_length='30', widget=forms.PasswordInput(attrs={'placeholder': 'Придумайте пароль'}))
	password2 = forms.CharField(label='Повторите пароль', max_length='30', widget=forms.PasswordInput(attrs={'placeholder': 'Повторите ваш пароль'}))

	def clean_password2(self):
		cd = self.cleaned_data

		if cd['password1'] != cd['password2']:
			raise forms.ValidationError("Пароли не совпадают")


class LoginForm(forms.Form):
	login = forms.CharField(label='Логин', max_length='30', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
	password = forms.CharField(label='Пароль', max_length='30', widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))


class CommentForm(forms.Form):
	title = forms.CharField(label='Придумайте заголовок комментарию или его тему', max_length=30)
	description = forms.CharField(label='Комментарий', widget=forms.Textarea())