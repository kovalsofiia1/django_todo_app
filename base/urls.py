from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),

    # Колекції
    path('collections/', views.collection_list, name='collection_list'),
    path('collections/add/', views.add_collection, name='add_collection'),
    path('collections/edit/<str:name>/', views.edit_collection, name='edit_collection'),
    path('collections/delete/<str:name>/', views.delete_collection, name='delete_collection'),
]
