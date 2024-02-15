from django.urls import path
from .views import TaskList,TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('',TaskList.as_view(), name='tasks'),   #'' for default url. tasklist is the view to load in case of default view.
    path('task/<int:pk>/',TaskDetail.as_view(), name='task'), # task/int_primary_key of the task 
    path('task-create/',TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(), name='task-delete'),
]
