from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm, UserProfileForm
from .models import Income, UserProfile
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


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Handle Income
    income, created_income = Income.objects.get_or_create(
        user=request.user,
        defaults={'amount': 0}
    )
    income_form = IncomeForm(instance=income)

    # Handle User Profile
    user_profile, created_profile = UserProfile.objects.get_or_create(user=request.user)
    profile_form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        if 'income_submit' in request.POST:
            income_form = IncomeForm(request.POST, instance=income)
            if income_form.is_valid():
                income_form.save()
        elif 'profile_submit' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user_profile)
            if profile_form.is_valid():
                profile_form.save()

    return render(request, 'accounts/profile.html', {
        'income_form': income_form,
        'profile_form': profile_form,
        'current_income': income.amount,
    })