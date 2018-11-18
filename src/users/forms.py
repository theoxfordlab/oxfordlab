from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm

from .models import User


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Password don't match")
        return pass2


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Password don't match")
        return pass2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "password", "active", "admin")

    def clean_password2(self):
        return self.initial["password"]


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text="First Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "first_name",
                "placeholder": "First Name",
                "autofocus": "autofocus",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Last Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "last_name",
                "placeholder": "Last Name",
            }
        ),
    )
    email = forms.CharField(
        max_length=254,
        required=True,
        help_text="Required",
        widget=forms.TextInput(
            attrs={"class": "form-control", "name": "email", "placeholder": "Email"}
        ),
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        help_text="Phone",
        widget=forms.TextInput(
            attrs={"class": "form-control", "name": "phone", "placeholder": "Phone"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "name": "password1",
                "placeholder": "Password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "name": "password2",
                "placeholder": "Confirm Password",
            }
        ),
    )

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Password don't match")
        return pass2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already taken.")
        return email

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "password1", "password2")
