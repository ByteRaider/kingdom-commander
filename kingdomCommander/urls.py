from django.urls import path
from . import views

urlpatterns = [
    ##########################
    ## For any Application  ##
    ##########################
    path('list_running_applications/', views.list_running_applications_view, name='list_running_applications'),
    path('connect_to_application/', views.connect_to_application_view, name='connect_to_application'),
    path('find_controls/', views.find_descendants_view, name='find_controls'),
    path('print_control_identifiers/', views.print_control_identifiers_view, name='print_control_identifiers'), 
    path('get_ui_elements/', views.get_ui_elements_view, name='get_ui_elements'), 
    path('get_child_window/', views.get_child_window_view, name='get_child_window'),
    path('get_child_window_control_identifiers/', views.get_child_window_control_identifiers_view, name='get_child_window_control_identifiers'),
  
    path('disconnect_from_application/', views.disconnect_from_application_view, name='disconnect_from_application'),
    path('close_application/', views.close_application_view, name='close_application'), # NOT TESTED!
]

##########################
## Rise of Kingdoms bot ##
##########################
urlpatterns += [
    path('connect_to_rise_of_kingdoms/', views.connect_to_rise_of_kingdoms_view, name='connect_to_rise_of_kingdoms'),

]