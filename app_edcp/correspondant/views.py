from django.shortcuts import render

# Create your views here.

# user/views.py
def index(request):
    """ Vue index demande correspondant """
    return render(request, 'correspondant/index.html')
