from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    city = forms.CharField(max_length=50, required=False)
    address = forms.CharField(max_length=50, required=False)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Account.objects.create(
                user=user,
                city=self.cleaned_data.get("city", ""),
                address=self.cleaned_data.get("address", "")
            )
        return user







