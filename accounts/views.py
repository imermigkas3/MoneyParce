from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout  # Import logout here
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {'title': 'Login'}

    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})

    elif request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')  # Update if this route doesn't exist

def signup(request):
    template_data = {'title': 'Sign Up'}

    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})

    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')  # Redirect to login page after successful signup
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})
