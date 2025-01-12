from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    email = forms.CharField(label='E-mail',
                            widget=forms.TextInput(attrs={'class': 'from-input'}))
    password = forms.CharField(label='Password',
                               widget=forms.TextInput(attrs={'class': 'from-input'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


class RegisterUserForm(UserCreationForm):
    email = forms.CharField(label="email", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Reenter the password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': "Имя",
            'last_name': "Фамилия",
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Such an E-mail already exists!")
        return email


class ProfileUserForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['avatar', 'biography', ]
