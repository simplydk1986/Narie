from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Notice, Qna

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class LoginForm(AuthenticationForm):
    pass
    
# --- CS Center Forms (NEW) ---

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15, 'placeholder': '내용을 입력하세요'}),
        }

class QnaForm(forms.ModelForm):
    class Meta:
        model = Qna
        fields = ['title', 'content', 'is_private']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요.'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': '문의 내용을 입력하세요.'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'is_private': '비밀글로 문의하기',
        }
