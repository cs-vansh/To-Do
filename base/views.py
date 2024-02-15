from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
#from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks') #show the task list when the user is logged in
    

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks') 
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs): #to let a user only access their own data and not someone else's data.
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''    # blank default value
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
        
        context['search_input']=search_input
        
        return context
    
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields =  ['title', 'description', 'complete']  # or use '__all__' incase you want to let user select from the list of users to create a task.
    success_url = reverse_lazy('tasks') # after successful task creation, send user back to tasks(list of all the tasks)
    
    def form_valid(self, form):               # function to restrict users for creating a task for some other user.
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields =  ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')