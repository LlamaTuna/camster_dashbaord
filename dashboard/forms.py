from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form that extends Django's built-in UserCreationForm.
    
    This form will allow new users to create an account by providing a username, email, 
    and password (with confirmation). It uses the User model from Django's authentication system.
    """
    
    class Meta:
        """
        Meta class to specify the model and fields that the form will use.
        
        This ensures that the form interacts with the built-in User model, and 
        the fields displayed on the form include username, email, password1, and password2.
        """
        model = User
        # The form is linked to the built-in User model in Django's authentication system.
        
        fields = ['username', 'email', 'password1', 'password2']
        # These fields will be displayed on the user creation form.
        # 'password1' is the initial password, and 'password2' is for confirmation.
