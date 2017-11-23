from django.contrib.auth.models import User
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime
from django.contrib.admin import widgets

class UserForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']

class ProfileForm(forms.ModelForm):
    profile_pic = forms.FileField()

    class Meta:
        model = User
        fields = ['profile_pic']


class AssignmentForm(forms.ModelForm):
    assignment_name = forms.CharField(max_length=250)
    assignment_file = forms.FileField()
    assignment_info = forms.CharField(max_length=500)
    deadline = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime)

    class Meta:
        model = User
        fields = ['assignment_name','assignment_info','assignment_name','deadline']


class MaterialForm(forms.ModelForm):
    material_name = forms.CharField(max_length=250)
    material_file = forms.FileField()
    material_info = forms.CharField(max_length=500)

    class Meta:
        model = User
        fields = ['material_name','material_file','material_info']

class TopicForm(forms.ModelForm):
    topic_name = forms.CharField(max_length=250)

    topic_info = forms.CharField(max_length=1000)

    class Meta:
        model = User
        fields = ['topic_name','topic_info']

class QuizForm(forms.ModelForm):
    quiz_name = forms.CharField(max_length=250)

    quiz_info = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['quiz_name','quiz_info']

