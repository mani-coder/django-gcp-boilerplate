# Standard Library Imports
import base64

# Third Party Library Imports
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_GET


def login(request):
    return render(request, "login.html")


@require_GET
def logout(request):
    auth_logout(request)
    redirect_url = (
        base64.b64decode(request.GET.get("b64redirect"))
        if request.GET.get("b64redirect")
        else request.GET.get("redirect")
    )
    if not redirect_url:
        redirect_url = settings.LOGOUT_REDIRECT_URL

    return redirect(redirect_url)
