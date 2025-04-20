from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def chat(request):
    user = request.user

    return render(request, 'agent/chat.html')