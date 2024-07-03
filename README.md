
// **Bitespeed Backend Task with Django and React**

// **1. Overview**
// **2. Setup Instructions**
// **3. Usage**
// **4. Hosting**

// **1. Overview**
This repository contains the implementation of the Bitespeed Backend Task using Django for the backend API and React for the frontend interface. The Bitespeed Backend Task project is a comprehensive implementation featuring a Python Django backend and a React.js frontend. The project addresses the requirements of an identification service that processes user information to establish primary and secondary contacts based on email and phone numbers. The backend leverages Django REST Framework to handle API requests and manage relational data, ensuring a robust and scalable server-side architecture. The frontend, built with React.js, provides a seamless user interface for submitting identification queries and displaying results dynamically. This project showcases advanced skills in full-stack development, integrating modern web technologies, and adhering to best practices for code quality and project structure. The solution is designed for ease of deployment and scalability, making it a reliable component in any larger system requiring contact identification services.

// **2. Setup Instructions**
// **2.1. Setup the Django Backend**
// **2.1.1. Create a Django Project**
```bash
django-admin startproject bitespeed_backend
cd bitespeed_backend
```

// **2.1.2. Create a Django App**
```bash
python manage.py startapp contact
```

// **2.1.3. Configure Database in settings.py**
Replace the default database configuration with your desired SQL database configuration, for example, PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bitespeed',
        'USER': 'your-username',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

// **2.1.4. Define the Contact Model in contact/models.py**
```python
from django.db import models

class Contact(models.Model):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linked_id = models.IntegerField(null=True, blank=True)
    link_precedence = models.CharField(max_length=10, default='primary')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
```

// **2.1.5. Create the Serializer in contact/serializers.py**
```python
from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
```

// **2.1.6. Create the View in contact/views.py**
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializers import ContactSerializer
from django.db.models import Q

class IdentifyView(APIView):
    def post(self, request):
        email = request.data.get('email')
        phone_number = request.data.get('phoneNumber')

        if not email and not phone_number:
            return Response({"error": "Email or phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        contacts = Contact.objects.filter(Q(email=email) | Q(phone_number=phone_number))
        primary_contact = None
        secondary_contacts = []

        if contacts exists():
            primary_contact = contacts.filter(link_precedence='primary').first() or contacts.first()
            secondary_contacts = contacts.filter(link_precedence='secondary')

            for contact in contacts:
                if contact.id != primary_contact.id:
                    contact.linked_id = primary_contact.id
                    contact.link_precedence = 'secondary'
                    contact.save()

        else:
            primary_contact = Contact.objects.create(email=email, phone_number=phone_number)

        primary_contact_serializer = ContactSerializer(primary_contact)
        secondary_contacts_serializer = ContactSerializer(secondary_contacts, many=True)

        response_data = {
            "contact": {
                "primaryContactId": primary_contact.id,
                "emails": list({primary_contact.email, *contacts.values_list('email', flat=True)}),
                "phoneNumbers": list({primary_contact.phone_number, *contacts.values_list('phone_number', flat=True)}),
                "secondaryContactIds": list(secondary_contacts.values_list('id', flat=True)),
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
```

// **2.1.7. Configure URLs in contact/urls.py**
```python
from django.urls import path
from .views import IdentifyView

urlpatterns = [
    path('identify/', IdentifyView.as_view(), name='identify'),
]
```

// **2.1.8. Include the App URLs in bitespeed_backend/urls.py**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('contact.urls')),
]
```

// **2.1.9. Install and Configure Django REST Framework**
Add Django REST Framework to your settings.py:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'contact',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}
```

// **2.1.10. Run Migrations and Start the Server**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

// **2.2. Setup the React Frontend**
// **2.2.1. Create a React App**
```bash
npx create-react-app bitespeed-frontend
cd bitespeed-frontend
```

// **2.2.2. Install Axios for HTTP Requests**
```bash
npm install axios
```

// **2.2.3. Create an Identify Component in src/components/Identify.js**

// **2.2.4. Update the App Component in src/App.js**


// **2.2.5. Run the React App**
```bash
npm start
```

// **3. Hosting**
// **3.1. Host the Django Backend**
- Push your Django backend code to a GitHub repository.
- Create a new web service on Render.com or any other hosting platform.
- Connect your GitHub repository.
- Set the build and start commands in the Render settings:
  - Build Command: `pip install -r requirements.txt && python manage.py migrate`
  - Start Command: `gunicorn bitespeed_backend.wsgi`

// **3.2. Host the React Frontend**
- Push your React frontend code to a GitHub repository.
- Create a new static site on Render.com or any other hosting platform.
- Connect your GitHub repository.
- Set the build command in the Render settings:
  - Build Command: `npm install && npm run build`
