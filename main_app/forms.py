from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from.models import Question, Survey


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

class QuestionCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Question
        fields = ['question_text', 'option_one', 'option_two', 'option_three']

class SurveyCreateForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['name', 'description', 'imageURL', 'owner']

class SurveyEditForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['name', 'description', 'imageURL']

class QuestionEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Question
        fields = ['question_text', 'option_one', 'option_two', 'option_three']
