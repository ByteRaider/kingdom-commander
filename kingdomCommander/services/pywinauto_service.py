from pywinauto import Application, Desktop

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

def connect_to_application(request, title=None, process_id=None, handle=None, class_name=None):
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
        raise ValueError("Either title, process_id, handle, or class_name must be provided")

    request.session['title'] = connected_app.window(best_match=title).window_text()
    return connected_app

def disconnect_from_application(app=connected_app):
    if app:
        app.kill()
        connected_app = None
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

## Rise of Kingdoms functions
def close_rise_of_kingdoms(app):
    window = app.window(title_re=".*Rise of Kingdoms")
    window.menu_select("File -> Exit")
    window.child_window(title="Don't Save", auto_id="CommandButton_7", control_type="Button").click()
    return "Rise of Kingdoms closed successfully."

def connect_to_rise_of_kingdoms():
    global connected_app
    connected_app = Application(backend="uia").connect(title_re=".*Rise of Kingdoms")
    request.session['title'] = connected_app.window(title_re=".*Rise of Kingdoms").window_text()
    return connected_app

def riseKingdoms():
    app = connect_to_rise_of_kingdoms(
    
    )
    return close_rise_of_kingdoms(app)
