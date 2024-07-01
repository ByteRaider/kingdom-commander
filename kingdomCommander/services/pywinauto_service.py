from pywinauto import Application, Desktop
import threading

connected_app = None


def list_running_applications():
    windows = Desktop(backend="uia").windows()
    running_apps = [{
        "title": win.window_text(),
        "class_name": win.class_name(),
        "automation_id": win.automation_id(),
        "process_id": win.process_id(),
        "handle": win.handle,
    } for win in windows]
    return running_apps

def connect_to_application(request):
    title = request.data.get('title')
    process_id = request.data.get('process_id')
    handle = request.data.get('handle')
    class_name = request.data.get('class_name')
    global connected_app
    if title:
        connected_app = Application(backend="uia").connect(best_match=title)
    elif process_id:
        connected_app = Application(backend="uia").connect(process=process_id)
    elif handle:
        connected_app = Application(backend="uia").connect(handle=handle)
    elif class_name:
        connected_app = Application(backend="uia").connect(class_name=class_name)
    else:
        raise ValueError(" FAILED CONNECTING TO APPLICATION")

    request.session['title'] = connected_app.window(best_match=title).window_text()
    return connected_app

def disconnect_from_application(app=connected_app):
    if app:
        #   app.kill() or app.close() or app.terminate() or app.quit() or app.stop() or app.hangup()
        connected_app = None
        request.session['title'] = None
        return {"status": "success", "message": "Disconnected from application"}
    else:
        return {"status": "error", "message": "No application is connected"}

def get_descendants(app, title):
    window = app.window(best_match=title)
    window.wait('visible')
    elements = window.descendants()
    controls_info = []
    for el in elements:
        control = {
            "name": el.window_text() if hasattr(el, 'window_text') else None,
            "control_type": el.control_type() if hasattr(el, 'control_type') else None,
            "automation_id": el.automation_id() if hasattr(el, 'automation_id') else None,
            "class_name": el.class_name() if hasattr(el, 'class_name') else None,
            "rect": {
                "left": el.rectangle().left,
                "top": el.rectangle().top,
                "right": el.rectangle().right,
                "bottom": el.rectangle().bottom
            } if hasattr(el, 'rectangle') else None,
            "is_enabled": el.is_enabled() if hasattr(el, 'is_enabled') else None,
            "is_visible": el.is_visible() if hasattr(el, 'is_visible') else None,
            "parent": el.parent().window_text() if hasattr(el, 'parent') and hasattr(el.parent(), 'window_text') else None,
            "handle": el.handle if hasattr(el, 'handle') else None,
        }
        if control:
            controls_info.append(control)
    return controls_info

def get_control_identifiers(window):
    # Import the io 
    import io
    # and sys modules
    import sys
    # to capture the output
    # since method is designed primarily for printing control identifiers to the console for debugging purposes
    # Create a string buffer to capture output
    buffer = io.StringIO()
    # Redirect stdout to the buffer
    sys.stdout = buffer

    try:
        # Call the pywinauto print_control_identifiers method
        window.print_control_identifiers()
    except Exception as e:
        return {"status": "error", "message": str(e)}

    # Restore stdout to its original state
    sys.stdout = sys.__stdout__
    # Get the content from buffer
    captured_output = buffer.getvalue()
    # Close the buffer
    buffer.close()

    elements = captured_output.split('\n')
    return elements

def get_elements_by_control_type(window, control_type):
    elements = window.children(control_type=control_type)
    element_data = []
    for el in elements:
        element_data.append({
            "window_text": el.window_text() if hasattr(el, 'window_text') else None,
            "automation_id": el.automation_id() if hasattr(el, 'automation_id') else None,
            "handle": el.handle if hasattr(el, 'handle') else None,
            "rect": {
                "left": el.rectangle().left,
                "top": el.rectangle().top,
                "right": el.rectangle().right,
                "bottom": el.rectangle().bottom
            } if hasattr(el, 'rectangle') else None
        })
    return element_data
    
def get_ui_elements(window):
    elements = {
        "images": get_elements_by_control_type(window, "Image"),
        "static_texts": get_elements_by_control_type(window, "Text"),
        "comboboxes": get_elements_by_control_type(window, "ComboBox"),
        "edit_fields": get_elements_by_control_type(window, "Edit"),
        "buttons": get_elements_by_control_type(window, "Button")
    }
    return elements

def get_images(window):
    return window.children(control_type="Image")

def get_static_texts(window):
    return window.children(control_type="Text")

def get_comboboxes(window):
    return window.children(control_type="ComboBox")

def get_edit_fields(window):
    return window.children(control_type="Edit")

def get_buttons(window):
    return window.children(control_type="Button")

def get_child_window_details(window, auto_id, control_type):
    child = window.child_window(auto_id=auto_id, control_type=control_type)
    try:
        details = {
            "window_text": child.window_text() if hasattr(child, 'window_text') else None,
            "automation_id": child.automation_id() if hasattr(child, 'automation_id') else None,
            "handle": child.handle if hasattr(child, 'handle') else None,
            "rect": {
                "left": child.rectangle().left,
                "top": child.rectangle().top,
                "right": child.rectangle().right,
                "bottom": child.rectangle().bottom
            } if hasattr(child, 'rectangle') else None
        }
        return {"status": "success", "details": details}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_child_window_control_identifiers(window, auto_id, control_type):
        # Import the io 
    import io
    # and sys modules
    import sys
    # to capture the output
    # since method is designed primarily for printing control identifiers to the console for debugging purposes
    # Create a string buffer to capture output
    buffer = io.StringIO()
    # Redirect stdout to the buffer
    sys.stdout = buffer
    try:
        if request.session['title'] and request.session['auto_id'] and request.session['control_type'] is not None:
            window.child_window(title = title, auto_id=auto_id, control_type=control_type).print_control_identifiers()
        else: 
            window.child_window(auto_id=auto_id, control_type=control_type).print_control_identifiers()
       
    except Exception as e:
        return {"status": "error", "message": str(e)}

    # Restore stdout to its original state
    sys.stdout = sys.__stdout__
    # Get the content from buffer
    captured_output = buffer.getvalue()
    # Close the buffer
    buffer.close()

    child = captured_output.split('\n')
    return {"status": "success", "control_identifiers": child}

####  wrapper objects #####
def get_child_window_wrapper_object(window):
    window.child_window(title = title, auto_id=auto_id, control_type=control_type).wrapper_object()
    return window.child_window_wrapper_object()

def get_element_wrapper_object(window, title=None, auto_id=None, control_type="Button", index=0, **kwargs):
    if title:
        matches = window.children(title=title, control_type=control_type, **kwargs)
    elif auto_id:
        matches = window.children(automation_id=auto_id, control_type=control_type, **kwargs)
    else:
        raise ValueError("Either title or auto_id must be provided to get a button")
    if len(matches) > 1:
        return matches[index].wrapper_object()
    else:
        return matches[0].wrapper_object()
####

