from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm, UserProfileForm
from .models import Income, UserProfile
from django.contrib.auth.models import User
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid_client import client
from django.http import JsonResponse
import json
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest

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

    balances = []
    if user_profile.access_token:
        try:
            balance_request = AccountsBalanceGetRequest(access_token=user_profile.access_token)
            balance_response = client.accounts_balance_get(balance_request)
            balances = balance_response['accounts']
        except Exception as e:
            print("Error fetching balances:", e)

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
        'balances': balances,
    })
import traceback
@login_required
def create_link_token(request):
    try:
        link_request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(
                client_user_id=str(request.user.id)
            ),
            client_name="MoneyParce",
            products=[
                Products("auth"),
                Products("transactions"),
                Products("identity"),
            ],
            country_codes=[CountryCode('US')],
            language='en',
        )
        response = client.link_token_create(link_request)
        return JsonResponse({'link_token': response['link_token']})
    except Exception as e:
        print("Error in Plaid Link Token creation:")
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=400)


from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

@csrf_exempt
@login_required
def exchange_public_token(request):
    data = json.loads(request.body)
    public_token = data['public_token']

    exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
    exchange_response = client.item_public_token_exchange(exchange_request)
    access_token = exchange_response['access_token']

    # Save to user profile
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.access_token = access_token
    user_profile.save()

    return JsonResponse({'message': 'Access token saved'})