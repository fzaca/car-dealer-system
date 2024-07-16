from django.http import JsonResponse
from django.views import View


class LoginAPIView(View):
    def post(self, request, *args, **kwargs):
        # TODO: Lógica de inicio de sesión para API
        return JsonResponse({"message": "Login successful"})


class LogoutAPIView(View):
    def post(self, request, *args, **kwargs):
        # TODO: Lógica de cierre de sesión para API
        return JsonResponse({"message": "Logout successful"})
