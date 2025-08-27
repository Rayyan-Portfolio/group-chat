from django.forms import ModelForm
from django import forms
from .models import *

class ChatMessageForm(ModelForm):
    class Meta:
        model = groupMessage
        fields = ['body']
        widgets = {
          'body': forms.TextInput(attrs={'placeholder': 'Type your message here...', 'class': 'p-4 text-black','rows': 1,  'maxlength': '300', 'autofocus': True}),
        }
      
    
