from django.shortcuts import render

# Create your views here.

# user/views.py
def index(request):
    """ Vue index demande autorisation """
    return render(request, 'demande_auto/index.html')
