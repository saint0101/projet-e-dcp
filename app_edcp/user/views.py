from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base_edcp.models import User

# Create your views here.

# user/views.py
def index(request):
    """ Vue index user """
    return render(request, 'user/index.html')


class UserListView(ListView):
    model = User
    template_name = 'user/user_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'user/user_detail.html'
    context_object_name = 'user'
