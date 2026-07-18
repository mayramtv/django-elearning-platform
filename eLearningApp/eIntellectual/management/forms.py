
from django import forms 

class SearchBoxForm(forms.Form):
    search_text = forms.CharField(label='Search', max_length=100)