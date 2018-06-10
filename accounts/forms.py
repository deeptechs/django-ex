from django import forms
from django.contrib.auth import authenticate
from accounts.models import MyUser


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150, label='Email Adress')
    password = forms.CharField(max_length=150, label='Password', widget=forms.PasswordInput)

    # Her form class ının kendi validation (clean) metodu vardır. Bunları override ederek uyarı mesajlarını verebiliriz.
    # Bu metod formda hata aldığımız zaman çalışır, auteticate hata aldırıp bunun çalışmasını sağlıyor.
    def clean(self):

        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Incorrect Mail or Password')
            return super(LoginForm, self).clean()


# Bu formu model formunda türetmek daha uygun çünkü gelen verileri user modeline uygun şekilde gelecek.
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=150, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=150, label='Password Confirm', widget=forms.PasswordInput)

    class Meta:
        model = MyUser

        # MyUser modelinden 3 alan bize lazım onları alıyoruz
        fields = [
            'email',
        ]

    # Form sınıflarının field validation ları için özel metodlar tanımlanır. Clean yazıp alttan tire vererek alan adı
    # yazılarak validation yapılabilir. Bu şekilde form kendini valide eder.
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords Missmatch!')
        return password2
