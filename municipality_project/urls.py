from django.urls import path

from . import views

app_name='municipality_project'
urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('authenticate', views.authenticate, name='authenticate'),
    path('info', views.info, name='info'),
    path('mytasks', views.my_tasks, name='mytasks'),
    path('activities', views.activities_view, name='activities'),
    path('create_activity', views.create_activity, name='create_activity'),
    path('create_task', views.create_task, name='create_task'),
    path('create_project', views.create_project, name='create_project'),
    path('save_task', views.save_task, name='save_task'),
    path('save_project', views.save_project, name='save_project'),
    path('project_task', views.project_task, name='project_task'),
    path('notifications', views.notifications_view, name='notifications'),
    path('activity/<int:activity_id>', views.activity_view, name='activityRow'),
    path('completeTask', views.completeTask_view, name='completeTask'),
]
