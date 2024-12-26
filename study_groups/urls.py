from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.study_group_list, name='study_group_list'),
    path('groups/create/', views.create_study_group, name='create_study_group'),
    path('groups/manage/<int:group_id>/', views.manage_study_group, name='manage_study_group'),
    path('groups/delete/<int:group_id>/', views.delete_study_group, name='delete_study_group'),
    path('groups/join/<int:group_id>/', views.join_study_group, name='join_study_group'),
    path('groups/leave/<int:group_id>/', views.leave_study_group, name='leave_study_group'),
    path('groups/members/<int:group_id>/', views.view_study_group_members, name='view_study_group_members'),
]
