from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from blogs.models import Post


# class RegistrationForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=30)
#     email = forms.EmailField(label='Email')
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password_confirm = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)
#
#     def clean_password_confirm(self):
#         if 'password' in self.cleaned_data:
#             password = self.cleaned_data['password']
#             password_confirm = self.cleaned_data['password_confirm']
#             if password == password_confirm and password:
#                 return password_confirm
#         raise forms.ValidationError("Invalid password!")
#
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if not re.search(r'^\w+$', username):
#             raise forms.ValidationError("Username contains special characters!")
#         try:
#             User.objects.get(username=username)
#         except ObjectDoesNotExist:
#             return username
#         raise forms.ValidationError("Username already exists!")
#
#     def save(self):
#         User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'],
#                                  password=self.cleaned_data['password'])


class NewPostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(), max_length=4000)
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'body', 'image']
