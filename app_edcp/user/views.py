from django.shortcuts import render

# Create your views here.

# user/views.py
def index(request):
    """ Vue index user """
    return render(request, 'user/index.html')
