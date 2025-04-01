from django import forms
from django.contrib.auth.forms import AuthenticationForm
from core.models import Project, Blog, Category

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ProjectForm(forms.ModelForm):
    technologies = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Django, React, PostgreSQL'})
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies', 'project_url', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        
class BlogForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="Select Category")

    class Meta:
        model = Blog
        fields = ['title', 'image', 'content', 'category']