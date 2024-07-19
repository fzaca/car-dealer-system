from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = CustomUser
		fields = ("username", "email", "is_staff")


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = ("username", "email", "is_staff")
