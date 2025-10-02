from django.urls import path
from . import views as views

app_name = 'staff'
urlpatterns = [
    path('', views.index, name='index'),
    path('edit_computer/<int:computer_id>/', views.edit_computer, name='edit_computer'),
    path('delete_computer/<int:computer_id>/', views.delete_computer, name='delete_computer'),
    path('computer_types/', views.computer_types, name='computer_types'),
    path('view_computer_type/<int:computer_id>/', views.view_computer_type, name='view_computer_type'),

    path('computer_list/', views.computer_list, name='computer_list'),
    path('computer_list/add/', views.computer_list_add, name='computer_list_add'),
    path('computer_list/edit/<int:computer_id>/', views.computer_list_edit, name='computer_list_edit'),
    path('computer_list/delete/<int:computer_id>/', views.computer_list_delete, name='computer_list_delete'),
]