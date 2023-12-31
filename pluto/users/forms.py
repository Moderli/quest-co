from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  
from .models import UserProfile, Question, Interest
from .models import Answer, Comment


class SignupForm(UserCreationForm):  
	email = forms.EmailField(max_length=200, help_text='Required')
	class Meta: 
		model = User
		fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'description', 'interests']



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'is_anonymous', 'question_description', 'tags']

    user_name = forms.CharField(max_length=50, required=False)
    is_anonymous = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    tags = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Separate tags with "#"'}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'description', 'interests']

    user = forms.CharField(max_length=50)
    description = forms.Textarea(attrs={'rows': 3})
    interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple)

# Add this to forms.py

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


