
from django import forms
from .models import Post, Category 

class BlogForm(forms.ModelForm):
    
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple 
    )


    class Meta:
        model = Post
        fields = ['title', 'body', 'categories', 'image']  # Add more fields as needed
    



class BlogRatingForm(forms.Form):
    rating = forms.DecimalField(max_digits=2, decimal_places=1, min_value=0, max_value=6)


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)