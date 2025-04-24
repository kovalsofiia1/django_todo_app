from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
path('welcome/', views.welcome, name='welcome'),

    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),

    # Колекції
    path('collections/', views.collection_list, name='collection_list'),
    path('collections/add/', views.add_collection, name='add_collection'),
    path('collections/edit/<int:col_id>/', views.edit_collection, name='edit_collection'),
    path('collections/delete/<int:col_id>/', views.delete_collection, name='delete_collection'),
]
