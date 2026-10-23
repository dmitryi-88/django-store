from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.password_validation import validate_password

from .models import EmailUser, UserProfile


class RegistrationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = EmailUser
        fields = ("email", "first_name", "last_name")

    city = forms.CharField(
        label="Город",
        max_length=100,
    )
    description = forms.CharField(
        label="О себе",
        widget=forms.Textarea,
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip()

        if EmailUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        if password2:
            validate_password(password2)

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

            UserProfile.objects.create(
                user=user,
                city=self.cleaned_data["city"],
                description=self.cleaned_data["description"],
            )

        return user
