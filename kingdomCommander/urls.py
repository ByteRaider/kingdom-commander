from django.urls import path
from . import views

urlpatterns = [
    path('list_running_applications/', views.list_running_applications_view, name='list_running_applications'),
    path('connect_to_application/', views.connect_to_application_view, name='connect_to_application'),
    path('find_controls/', views.find_controls_view, name='find_controls'),
    path('disconnect_from_application/', views.disconnect_from_application_view, name='disconnect_from_application'),
    path('close_application/', views.close_application_view, name='close_application'), # NOT TESTED!
]