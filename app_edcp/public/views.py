from django.shortcuts import render

# Create your views here.


def index(request):
    """ Vue interface publique (home)"""
    return render(request, 'public/index.html')


def a_propos(request):
    """ Vue page à propos"""
    return render(request, 'public/a-propos.html')


def guides(request):
    """ Vue page guides"""
    return render(request, 'public/guides.html')


def faq(request):
    """ Vue page F.A.Q"""
    return render(request, 'public/faq.html')


def contacts(request):
    """ Vue page contacts"""
    return render(request, 'public/contacts.html')