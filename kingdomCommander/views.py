import threading
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services.riseOfKingdoms_service import (rise_of_kingdoms_bot)
from .services.pywinauto_service import (
    get_descendants,  
    list_running_applications,
    connect_to_application,
    disconnect_from_application,
    get_control_identifiers,
    get_ui_elements,
    get_elements_by_control_type, 
    get_child_window_details,
    get_child_window_control_identifiers,
    
)
from .serializers import (ControlInfoSerializer, RectSerializer,
RunningApplicationSerializer,ImageSerializer,StaticTextSerializer,ComboBoxSerializer, EditFieldSerializer, ButtonSerializer,
UIElementsSerializer, ChildWindowSerializer
)

# Lock for ensuring single access to the application
app_lock = threading.Lock()


@api_view(['GET'])
def list_running_applications_view(request):
    running_apps = list_running_applications()
    serializer = RunningApplicationSerializer(running_apps, many=True)
    return Response({"status": "success", "applications": serializer.data})

@api_view(['POST'])
def connect_to_application_view(request):
    title = request.data.get('title')
    process_id = request.data.get('process_id')
    handle = request.data.get('handle')
    class_name = request.data.get('class_name')

    if not (title or process_id or handle or class_name):
        return Response({"status": "error", "message": "Either title, process_id, handle, or class_name must be provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    with app_lock:
        try:
            app = connect_to_application(request)
            return Response({"status": "success", "message": f"Connected to application with the information provided. title: {title}, process_id: {process_id}, handle: {handle}, or class_name: {class_name}"})
        except Exception as e:
            return Response({"status": "error", "message": f"Failed to connect to application. Error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def find_descendants_view(request):
    try:
        title = request.data.get('title')
        if not title:
            title = request.session['title']
    except AttributeError:
        return Response({"status": "error", "message": " Application Window  Title is required to find controls."}, status=status.HTTP_400_BAD_REQUEST)

    with app_lock:
        #app = connect_to_rise_of_kingdoms()
        app = connect_to_application(request)
        #print(f'APPLICATION CONNECTED IS    : {app}')
        controls_info = get_descendants(app, title)
        serializer = ControlInfoSerializer(controls_info, many=True)
        return Response({"status": "success", "controls": serializer.data})

@api_view(['POST'])
def print_control_identifiers_view(request):
    title = request.data.get('title')
    process_id = request.data.get('process_id')
    handle = request.data.get('handle')
    class_name = request.data.get('class_name')

    if not (title or process_id or handle or class_name):
        return Response({"status": "error", "message": "Either title, process_id, handle, or class_name must be provided"}, status=status.HTTP_400_BAD_REQUEST)

    with app_lock:
        try:
            app = connect_to_application(request)
            window = app.window(best_match=title)
            control_identifiers = get_control_identifiers(window)
            #serializer = PrintControlIdentifiersSerializer({"control_identifiers": control_identifiers})
            #return Response({"status": "success", "control_identifiers": serializer.data['control_identifiers']})
            return Response({"status": "success", "control_identifiers": control_identifiers})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def get_ui_elements_view(request):
    title = request.data.get('title')
    process_id = request.data.get('process_id')
    handle = request.data.get('handle')
    class_name = request.data.get('class_name')

    if not (title or process_id or handle or class_name):
        return Response({"status": "error", "message": "Either title, process_id, handle, or class_name must be provided"}, status=status.HTTP_400_BAD_REQUEST)

    with app_lock:
        try:
            app = connect_to_application(request)
            window = app.window(best_match=title)
            elements = get_ui_elements(window)
            
            serializer = UIElementsSerializer(elements)
            return Response({"status": "success", "elements": serializer.data})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def get_child_window_view(request):
    title = request.data.get('title')
    process_id = request.data.get('process_id')
    handle = request.data.get('handle')
    class_name = request.data.get('class_name')
    auto_id = request.data.get('auto_id')
    control_type = request.data.get('control_type')


    if not control_type:
        return Response({"status": "error", "message": "control_type must be provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not auto_id:
        return Response({"status": "error", "message": "auto_id must be provided"}, status=status.HTTP_400_BAD_REQUEST)
    with app_lock:
        try:
            app = connect_to_application(request)
            window = app.window(best_match=title)
            details = get_child_window_details(window, auto_id, control_type)
            if details["status"] == "error":
                return Response(details, status=status.HTTP_400_BAD_REQUEST)
            serializer = ChildWindowSerializer(details["details"])
            return Response({"status": "success", "details": serializer.data})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def get_child_window_control_identifiers_view(request):
    title = request.data.get('title')
    #process_id = request.data.get('process_id')
    #handle = request.data.get('handle')
    #class_name = request.data.get('class_name')
    auto_id = request.data.get('auto_id')
    control_type = request.data.get('control_type')

    if not (auto_id and control_type):
        return Response({"status": "error", "message": "Both auto_id and control_type must be provided"}, status=status.HTTP_400_BAD_REQUEST)

    with app_lock:
        if control_type and auto_id:
            try:
                if title in request.session:
                    app =  connect_to_application(request.session[title])
                else:
                    # connect to app and send title in the request
                    try:
                        app = connect_to_application(request)
                    except Exception as e:
                        return Response({"status": "error", "message": f" Failed to connect to application. Error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                window = app.window(best_match=title)
                window_child = get_child_window_control_identifiers(window, auto_id, control_type)
                result = window_child 
                if result["status"] == "error":
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                return Response({"status": "success", f"{control_type}s": result["control_identifiers"]})
            except Exception as e:
                return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def close_application_view(request):
    with app_lock:
        #app = connect_to_rise_of_kingdoms()
        app = connect_to_application()
        response_message = close_rise_of_kingdoms(app)
        return Response({"status": "success", "message": response_message})

@api_view(['POST'])
def disconnect_from_application_view(request):
    with app_lock:
        response_message = disconnect_from_application()
        return Response({"status": "success", "message": response_message})

