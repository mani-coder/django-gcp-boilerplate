"""
URL configuration for Django-GCP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Third Party Library Imports
import debug_toolbar
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# Same App Imports
from .graphql.views import CustomGraphQLView
from .graphql.views import GraphiQLView

# Project Imports
from accounts.views import login
from accounts.views import logout
from app.views import streamer_test
from app.views import streamer_test_page


urlpatterns = [
    path("admin/", admin.site.urls),
    # API
    path("api/logout/", logout, name="logout"),
    path("api/stream/test/", streamer_test, name="stream-api-test"),
    # Dev
    path("dev/login", login, name="dev-login"),
    path("dev/streamer/", streamer_test_page, name="streamer"),
    # GQL
    path("graphql/", csrf_exempt(CustomGraphQLView.as_view(graphiql=False))),
    path("graphiql/", GraphiQLView.as_view()),
    path("__debug__/", include(debug_toolbar.urls)),
    path("", include("tasks.urls")),
]
