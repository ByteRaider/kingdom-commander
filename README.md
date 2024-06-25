# Kingdom Commander

Kingdom Commander is a Django-based service that uses `pywinauto` to automate interactions with any Windows application. It allows you to connect to a running application, list controls, and perform actions through a REST API.

![Kingdom Commander](https://i.postimg.cc/Kckc0HfV/DALL-E-2024-06-25-12-16-03-A-bird-s-eye-view-of-a-futuristic-giant-robot-leading-an-ancient-Roman.png?text=Kingdom+Commander+Logo)

## Table of Contents

- [Features](##Features)
- [Prerequisites](##Prerequisites)
- [Installation](##Installation)
- [Running the Project](#Running-the-project)
- [API Endpoints](##Api-endpoints)
- [Usage Examples](##Usage-examples)

## Features

- List running applications.
- Connect to a running application by title, process ID, handle, or class name.
- List controls of a connected application.
- Disconnect from a connected application.
- Close a connected application.


## Prerequisites

- Python 3.12.4
- Django 5.0.6
- `pywinauto` library
- Django REST framework

## Project Structure
####KingdomCommander/
├── manage.py
├── README.md
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
├── kingdomCommander/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   ├── services/
│       ├── pywinauto_service.py
│   ├── tests/
│       ├── __init__.py
│       ├── test_views.py
│       ├── test_services.py
├── static/
│   └── ...
└── templates/
    └── ...

## Installation

1. **Clone the repository:**
```
   git clone https://github.com/yourusername/kingdom-commander.git
   cd kingdom-commander
```

2. **Create a virtual environment and activate it:**
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the dependencies:**
```
pip install -r requirements.txt
```
4. **Apply the migrations:**
```
python manage.py migrate
```
5. **Create a superuser to access the Django admin (optional but recommended):**
```
python manage.py createsuperuser
```

## Running the Project
1. **Start the Django development server**
```
python manage.py runserver
```
2. **Access the API at http://127.0.0.1:8000/api/.**

#API Endpoints

##List Running Applications
- URL: /api/list_running_applications/
- Method: **GET**
- Description: Lists all running applications.
- Request Body: None

Usage Example:
```
curl -X GET http://127.0.0.1:8000/api/list_running_applications/
```
Response:
```
{
  "status": "success",
  "applications": [...]
}
```


##Connect to Application
URL: /api/connect_to_application/
- Method: **POST**
- Description: Connects to a running application.
- Request Body: ```{  "title": "application title",  "process_id": "application process ID",  "handle": "application handle",  "class_name": "application class name"}``` At least one parameter is required.

Usage Example:
```
curl -X POST http://127.0.0.1:8000/api/connect_to_application/ \
     -H "Content-Type: application/json" \
     -d '{"title": "Notepad"}'
```
Response
```
{
  "status": "success",
  "message": "Connected to application with title: ..."
}
```

##Find Controls
- URL: /api/find_controls/
- Method: POST
- Description: Finds and lists controls of the connected application.
- Request Body:``` { "title": "application title"}```

Usage Example:
```
curl -X POST http://127.0.0.1:8000/api/find_controls/ \
     -H "Content-Type: application/json" \
     -d '{"title": "Notepad"}'
```

Response:

```
{
  "status": "success",
  "controls": [...]
}
```
##Disconnect from Application
- URL: /api/disconnect_from_application/
- Method: **POST**
- Description: Disconnects from the connected application.
- Request Body: **None**

Usage Example:
```
curl -X POST http://127.0.0.1:8000/api/disconnect_from_application/
```

Response:
```
{
  "status": "success",
  "message": "Disconnected from application."
}
```

###Close Application
- URL: /api/close_application/
- Method: **POST**
- Description: Closes the connected application.
- Request Body: **None**

Usage Example:
```
curl -X POST http://127.0.0.1:8000/api/close_application/
```

Response:
```
{
  "status": "success",
  "message": "Application closed successfully."
}```
