from django import forms
from django.contrib.auth.models import User
from game.models import UserProfile, Post, Announcement


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    phone_no = forms.CharField(max_length=UserProfile.PHONE_NO_MAX_LENGTH)

    class Meta:
        model = UserProfile
        fields = ('phone_no',)

#
# class PostForm(forms.ModelForm):
#     title = forms.CharField(max_length=100)
#     content = forms.CharField(max_length=500)
#
#     class Meta:
#         model = Post
#         fields = ('title', 'content',)


class AnnouncementForm(forms.ModelForm):
    title = forms.CharField(max_length=Announcement.TITLE_MAX_LENGTH,
                            help_text="Please enter the title of announcement")
    content = forms.CharField(max_length=Announcement.CONTENT_MAX_LENGTH,
                              help_text="Please enter the content of announcement")

    class Meta:
        model = Announcement
        fields = ('title', 'content', )
