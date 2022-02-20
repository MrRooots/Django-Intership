from webbrowser import get

from django.http import HttpResponse

from django.conf import settings

# Custom api auth middleware
class ApiAuthMiddleware:
  def __init__(self, get_response) -> None:
    self.get_response = get_response

  def __call__(self, request):
    if request.headers.get('API-KEY', '') == settings.API_KEY:
      return self.get_response(request)
    else:
      return HttpResponse('401 Unauthorized', status=401)
