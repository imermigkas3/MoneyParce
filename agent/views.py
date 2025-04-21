from django.shortcuts import render
from .forms import ChatForm

# Create your views here.
def chat(request):
    user = request.user

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            request.session['message_list'].append(form.cleaned_data['your_message'])
            request.session.modified = True
    else: # first time we visit the chat page
        request.session['message_list'] = []
    form = ChatForm()

    return render(request, 'agent/chat.html', {'form': form,
                                               'message_list': request.session['message_list']})