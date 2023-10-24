from django import forms
from django.contrib.auth.forms import UserCreationForm
from NFTapp.models import User, NFTProduct, Topic,\
                             NFTProductOwner, Type, NFTBlog, \
                                BlogSection, BlogComment, ProductComment,\
                                FAQ, FAQTitle, NFTProductFavorite

# class MyUserCreationForm(UserCreationForm, forms.ModelForm):
#     name = forms.CharField(widget=forms.TextInput, label="Name")
#     username = forms.CharField(widget=forms.TextInput, label="Username")
#     email = forms.EmailField(widget=forms.EmailInput, label="Email")
#     bio = forms.CharField(
#         widget=forms.Textarea(),
#         label="Bio",
#         max_length=500 
#     )
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")
#     confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

#     class Meta:
#         model = User
#         fields = ['name', 'username', 'email', 'bio', 'password', 'confirm_password']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2', 'bio']