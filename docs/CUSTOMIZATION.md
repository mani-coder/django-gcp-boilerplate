# Customization Guide

This guide explains how to customize the Django-GCP boilerplate for your specific needs.

## Project Structure Overview

```
backend/core/
├── app/                    # Main Django configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   ├── graphql/           # GraphQL schema and views
│   ├── assets/            # Static assets
│   └── templates/         # HTML templates
├── accounts/              # User authentication app
├── deploy/                # GCP deployment utilities
├── tasks/                 # Cloud Tasks integration
└── utils/                 # Shared utilities
```

## Creating New Django Apps

### 1. Create App

```bash
cd backend/core
python manage.py startapp myapp
```

### 2. Add to INSTALLED_APPS

Edit `app/settings.py`:

```python
INSTALLED_APPS = [
    ...
    "myapp",
]
```

### 3. Create Models

Edit `myapp/models.py`:

```python
from django.db import models
from accounts.models import User

class MyModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

### 4. Create and Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Register in Admin

Edit `myapp/admin.py`:

```python
from django.contrib import admin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    search_fields = ['name']
```

## Adding GraphQL Types

### 1. Create GraphQL Types

Create `myapp/gql/types.py`:

```python
import graphene
from graphene_django import DjangoObjectType
from myapp.models import MyModel

class MyModelType(DjangoObjectType):
    class Meta:
        model = MyModel
        fields = '__all__'
```

### 2. Create Queries

Create `myapp/gql/queries.py`:

```python
import graphene
from myapp.models import MyModel
from .types import MyModelType

class Query(graphene.ObjectType):
    my_models = graphene.List(MyModelType)
    my_model = graphene.Field(MyModelType, id=graphene.Int())

    def resolve_my_models(self, info):
        return MyModel.objects.all()

    def resolve_my_model(self, info, id):
        return MyModel.objects.get(id=id)
```

### 3. Create Mutations

Create `myapp/gql/mutations.py`:

```python
import graphene
from myapp.models import MyModel
from .types import MyModelType

class CreateMyModel(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    my_model = graphene.Field(MyModelType)

    def mutate(self, info, name):
        user = info.context.user
        my_model = MyModel.objects.create(user=user, name=name)
        return CreateMyModel(my_model=my_model)

class Mutation(graphene.ObjectType):
    create_my_model = CreateMyModel.Field()
```

### 4. Update Main Schema

Edit `app/graphql/schema.py`:

```python
import graphene
from accounts.gql.schema import Query as AccountsQuery
from accounts.gql.schema import Mutation as AccountsMutation
from myapp.gql.queries import Query as MyAppQuery
from myapp.gql.mutations import Mutation as MyAppMutation

class Query(AccountsQuery, MyAppQuery, graphene.ObjectType):
    pass

class Mutation(AccountsMutation, MyAppMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
```

## Adding REST API Endpoints

### 1. Create Serializers

Create `myapp/serializers.py`:

```python
from rest_framework import serializers
from myapp.models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']
```

### 2. Create Views

Create `myapp/views.py`:

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from myapp.models import MyModel
from myapp.serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
```

### 3. Create URLs

Create `myapp/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import MyModelViewSet

router = DefaultRouter()
router.register('models', MyModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### 4. Include in Main URLs

Edit `app/urls.py`:

```python
urlpatterns = [
    ...
    path('', include('myapp.urls')),
]
```

## Adding Cloud Tasks

### 1. Define Task Function

Create `myapp/tasks.py`:

```python
import logging

logger = logging.getLogger(__name__)

def process_my_task(item_id):
    """Process a background task"""
    logger.info(f"Processing task for item {item_id}")
    # Your task logic here
    return True
```

### 2. Queue Task

In your view or mutation:

```python
from tasks.queue import queue_async_task, TaskPayload
from myapp.tasks import process_my_task

# Queue the task
queue_async_task(TaskPayload(
    function=process_my_task,
    kwargs={"item_id": 123},
    seconds=0  # immediate, or delay in seconds
))
```

### 3. Register Task Handler

Tasks are automatically discovered if they follow the pattern above.

## Custom Middleware

### Create Middleware

Create `myapp/middleware.py`:

```python
class MyCustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code before view
        response = self.get_response(request)
        # Code after view
        return response
```

### Add to Settings

Edit `app/settings.py`:

```python
MIDDLEWARE = [
    ...
    'myapp.middleware.MyCustomMiddleware',
]
```

## Custom Management Commands

### Create Command

Create `myapp/management/commands/my_command.py`:

```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description of my command'

    def add_arguments(self, parser):
        parser.add_argument('--option', type=str, help='An option')

    def handle(self, *args, **options):
        self.stdout.write('Running command...')
        # Command logic here
        self.stdout.write(self.style.SUCCESS('Done!'))
```

### Run Command

```bash
python manage.py my_command --option=value
```

## Environment-Specific Settings

### Override Settings

Create `app/settings_local.py` for local overrides:

```python
from .settings import *

# Local overrides
DEBUG = True
ALLOWED_HOSTS = ['*']
```

### Use Different Settings

```bash
python manage.py runserver --settings=app.settings_local
```

## Adding Third-Party Packages

### 1. Add to requirements.txt

```txt
celery==5.3.4
django-redis==5.4.0
```

### 2. Install

```bash
pip install -r requirements.txt
```

### 3. Configure

Edit `app/settings.py`:

```python
# Redis Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisBackend',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
    }
}
```

## Custom User Model Extensions

### Extend User Model

Edit `accounts/models.py`:

```python
class User(AbstractBaseUser, PermissionsMixin):
    # Existing fields...

    # Add custom fields
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # Don't forget to create migrations
```

### Create Migration

```bash
python manage.py makemigrations accounts
python manage.py migrate accounts
```

## File Uploads to GCS

### Configure Model

```python
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

Files will automatically upload to GCS when `USE_GCS=True` in settings.

### Direct Upload from Frontend

For large files, use signed URLs:

```python
from google.cloud import storage
from datetime import timedelta

def generate_signed_url(blob_name):
    """Generate a signed URL for direct upload"""
    client = storage.Client()
    bucket = client.bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=15),
        method="PUT",
    )
    return url
```

## Testing

### Create Tests

Create `myapp/tests.py`:

```python
from django.test import TestCase
from accounts.models import User
from myapp.models import MyModel

class MyModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            firebase_uid='test-uid',
            password='testpass'
        )

    def test_create_model(self):
        obj = MyModel.objects.create(
            user=self.user,
            name='Test'
        )
        self.assertEqual(obj.name, 'Test')
```

### Run Tests

```bash
python manage.py test
python manage.py test myapp  # Test specific app
python manage.py test myapp.tests.MyModelTestCase  # Test specific case
```

## Logging

### Configure App-Level Logging

Edit `app/settings.py`:

```python
LOGGING['loggers']['myapp'] = {
    'handlers': ['console'],
    'level': 'DEBUG' if DEBUG else 'INFO',
}
```

### Use in Code

```python
import logging

logger = logging.getLogger(__name__)

logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
```

## Database Optimization

### Add Indexes

```python
class MyModel(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['user', 'created_at']),
        ]
```

### Use select_related and prefetch_related

```python
# select_related for ForeignKey
MyModel.objects.select_related('user').all()

# prefetch_related for ManyToMany
MyModel.objects.prefetch_related('tags').all()
```

## Changing Project Name

To rename the project from `app` to something else:

### 1. Rename Directory

```bash
mv backend/core/app backend/core/mynewname
```

### 2. Update Settings

Replace `APP_NAME = "app"` with `APP_NAME = "mynewname"` in `mynewname/settings.py`

### 3. Update Imports

Find and replace all imports:
```bash
find . -name "*.py" -exec sed -i 's/from app\./from mynewname./g' {} +
find . -name "*.py" -exec sed -i 's/import app\./import mynewname./g' {} +
```

### 4. Update manage.py

Update `DJANGO_SETTINGS_MODULE` in `manage.py`

## Next Steps

- Review [Security Best Practices](https://docs.djangoproject.com/en/5.1/topics/security/)
- Optimize [Database Queries](https://docs.djangoproject.com/en/5.1/topics/db/optimization/)
- Implement [Caching](https://docs.djangoproject.com/en/5.1/topics/cache/)
- Set up [Monitoring & Alerting](https://cloud.google.com/monitoring/docs)
