from django.shortcuts import render

# Create your views here.
def index(request):
    #we use this dictionary to pass information from view functions to templates
    template_data = {}
    template_data['title'] = 'Money Parce'
    return render(request, 'home/index.html', {'template_data' : template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {
        'template_data' : template_data})