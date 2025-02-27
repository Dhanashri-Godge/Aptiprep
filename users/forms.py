from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    class Meta:
        model = CustomUser
        # Use 'username' (from AbstractUser), 'email', and 'role'
        fields = ("username", "email", "role")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap styling
        for field in self.fields:
            self.fields[field].widget.attrs.setdefault("class", "form-control")

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"}),
        label="Username"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(self.request, username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password.")
        return cleaned_data
