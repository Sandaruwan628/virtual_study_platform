from django import forms
from .models import Whiteboard

class WhiteboardForm(forms.ModelForm):
    class Meta:
        model = Whiteboard
        fields = ['name']  # Only the name is required during creation
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Whiteboard Name'}),
        }
