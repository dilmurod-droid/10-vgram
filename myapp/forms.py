from django import forms
from django.contrib.auth.models import User
from .models import Post, Profile, ChatMessage

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']

class UserRegisterProfileForm(forms.ModelForm):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    bio = forms.CharField(widget=forms.Textarea)
    profile_pic = forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'profile_pic']

    def save(self, commit=True):
        user = super(UserRegisterProfileForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            Profile.objects.create(user=user, bio=self.cleaned_data['bio'], profile_pic=self.cleaned_data['profile_pic'])
        return user
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'video']

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
