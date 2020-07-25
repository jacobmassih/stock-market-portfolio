from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages	

def register(request):

	if request.user.is_authenticated:
		return redirect('main')
	else:
		form = UserCreationForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, 'Account Successfuly Created. Log in to continue')
			return redirect('login')

		return render(request, 'registration/register.html', {'form' : form})