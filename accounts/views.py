from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.views.generic import FormView
from photo.models import Album


# Create your views here.


# Class Based Login View
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/form.html'

    # Template tarafının context dataya ulaşması için bu metodu dolduruyoruz
    def get_context_data(self, **kwargs):
        print("Context e girdim")
        context = super(LoginView, self).get_context_data(**kwargs)
        context.update({'title': 'Login'})
        return context

    # Form validasyonunu yapıyor, hata atarsa formun clean metodu çalışıyor
    def form_valid(self, form):
        print("Validasyona girdim")
        request = self.request
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        # authenticate yanlış loginde hata fırlatır, form bunu yakalar ve clean metodu ile validasyona verir.
        user = authenticate(username=email, password=password)
        # Hata alınmaz ise kullanıcıyı login et ve anasayfaya yönlen
        login(request, user)
        return redirect('home:home')


# Funtion Based Login View
# def login_view(request):
#     # Login olunmuş ise ana sayfaya
#     if request.user.is_authenticated:
#         return redirect('home:home')
#
#     form = LoginForm(request.POST or None)
#     if form.is_valid():
#         email = form.cleaned_data.get('email')
#         password = form.cleaned_data.get('password')
#         # authenticate yanlış loginde hata fırlatır, form bunu yakalar ve clean metodu ile validasyona verir.
#         user = authenticate(username=email, password=password)
#         # Hata alınmaz ise kullanıcıyı login et ve anasayfaya yönlen
#         login(request, user)
#         return redirect('home:home')
#
#     context = {
#         'form': form,
#         'title': 'Login'
#     }
#
#     return render(request, 'accounts/form.html', context)


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        # Form user modelden türediği için save metodu user objesini dönüyor
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        # user.is_staff = True Yönetici sayfasına giriş hakkı
        # user.is_superuser = True Yönetici sayfasında değişiklik hakkı
        user.save()
        new_user = authenticate(username=user.email, password=password)
        login(request, new_user)
        # Register olan her kullanıcının default bir albümü olmalı ! Tüm fotolar buna atılacak
        Album.set_default_album(user)
        return redirect('home:home')

    context = {
        'form': form,
        'title': 'Register'
    }

    return render(request, 'accounts/form.html', context)


def logout_view(request):
    logout(request)
    return redirect('home:home')
