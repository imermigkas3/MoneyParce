from django.shortcuts import render
from .forms import ChatForm
from google import genai
from config import API_KEY

# Create your views here.
def chat(request):
    client = genai.Client(api_key=API_KEY)

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            request.session['message_list'].append(form.cleaned_data['your_message'])
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=form.cleaned_data['your_message']
            )
            request.session['message_list'].append(response.text)
            request.session.modified = True
    else: # first time we visit the chat page
        request.session['message_list'] = []
    form = ChatForm()

    return render(request, 'agent/chat.html', {'form': form,
                                               'message_list': request.session['message_list']})