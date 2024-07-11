from django.shortcuts import render

# Create your views here.

# user/views.py
def index(request):
    """ Vue index demande enregistrenent """
    return render(request, 'enregistrement/index.html')
