from django import forms
from .models import Livre

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['Name_book', 'Authour_name', 'Genre', 'Image', 'Stock', 'Prix']
        

