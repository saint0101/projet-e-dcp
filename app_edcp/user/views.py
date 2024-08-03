from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib import messages
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


class UserUpdateView(UpdateView):
    model = User
    fields = [
        'nom',
        'prenoms',
        'email',
        'telephone',
        'organisation',
    ]
    
    template_name = 'user/user_edit.html'
    context_object_name = 'user'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Vos informations ont été mises à jour.')
        return response
    
    def get_success_url(self):
        # Redirect to the detail view of the created object
        return reverse('dashboard:user:detail', kwargs={'pk': self.object.pk})