"""
URL configuration for MoneyParce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # include function includes URLs form other URL configuration files (namely the home app here)
    # The empty string, '', represents the base URL to include the URLs from the home.urls file.

    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include("django.contrib.auth.urls")),
    path('transactions/', include('transactions.urls')),
    path('budgets/', include('budgets.urls')),
    path('agent/', include('agent.urls')),
    path('transactions/', include('transactions.urls')),
    path('', include('analytics.urls')),

]
