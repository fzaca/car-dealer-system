from django.http import JsonResponse
from django.views import View


class LoginAPIView(View):
	def post(self, request, *args, **kwargs):  # noqa: PLR6301, E501
		# TODO: Lógica de inicio de sesión para API # noqa: ERA001
		return JsonResponse({"message": "Login successful"})


class LogoutAPIView(View):
	def post(self, request, *args, **kwargs):  # noqa: PLR6301, E501
		# TODO: Lógica de cierre de sesión para API # noqa: ERA001
		return JsonResponse({"message": "Logout successful"})


class RegisterAPIView(View):
	def post(self, request, *args, **kwargs):  # noqa: PLR6301, E501
		# TODO: Lógica de registro para API # noqa: ERA001
		return JsonResponse({"message": "Register successful"})
