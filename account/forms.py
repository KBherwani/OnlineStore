from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
    """
        Used to manage custom Login form view
    """

    email = forms.EmailField(
        required=True,
        error_messages={
            'invalid': "Please enter a valid email address.",
            'required': "Please enter an email address."
        })
    password = forms.CharField(required=True,
                               error_messages={
                                   'required': "Please enter a password.",
                               }
                               )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            if not User.objects.filter(
                    email=email
            ).exists():
                raise ValidationError("User with this email is not exist.")

            user_obj = User.objects.get(
                email=email
            )
            if not user_obj.check_password(password):
                raise ValidationError("Please enter correct password.")
            if not user_obj.is_active:
                raise ValidationError(
                    "Your account is Inactive. Please check your registered "
                    "email for account activation.")
            # self.user = userprofile_obj.user
            return user_obj
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save()