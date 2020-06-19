from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('update_tasks/<str:pk>', views.updateTask, name='update-task'),
    path('delete_tasks/<str:pk>', views.deleteTask, name='delete-task'),
    path('calculator/', views.calculator, name='calculator'),
    path('practice/', views.practice, name='practice'),
]