from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
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
    bio = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':5}))

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2', 'bio']

class UserForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':5}))

    class Meta:
        model = User
        fields = ['cover_photo', 'avatar', 'name', 'username', 'email', 'bio']

class UpdatePasswordForm(PasswordChangeForm):
    # def __init__(self, *args, **kwargs):
    #     super(PasswordChangeForm, self).__init__(*args, **kwargs)
    #     self.fields['new_password1'].label = 'New Password'
    #     self.fields['new_password2'].label = 'Password confirmed'
    class Meta:
        model = User  
        fields = ['old_password', 'new_password1', 'new_password2']