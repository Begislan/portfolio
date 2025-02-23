from django.urls import reverse_lazy
from django.views.generic import CreateView
from core.models import CustomUser as User
from adminka.views import profile
from .forms import CustomUserCreationForm
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib import messages
import requests

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def logout_view(request):
    logout(request)
    return redirect('core') # на главную страницу сайта


def login_user(request):
    print("shag")
    if request.method == "POST":
        print('shag 0')
        form_data = {
            'email': request.POST['username'],
            'password': request.POST['password'],
        }
        res = requests.post('https://api.myedu.oshsu.kg/public/api/login', form_data)
        email = request.POST['username']
        print(form_data)
        print(res)
        print('Shag 2')
        if res.status_code == 200:
            print('res status code')
            token = res.json()['authorisation']['token']
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",  # Указываем тип контента, если нужно
            }
            userinfo = requests.get('https://api.myedu.oshsu.kg/public/api/user/', headers=headers)
            getuser = userinfo.json()['user']
            email = getuser['email']
            password = request.POST['password']
            username = getuser['last_name'] + ' ' + getuser['name']
            # print(getuser['email'])
            is_exists = User.objects.filter(email=email).exists()

            if not is_exists:
                user = User.objects.create(
                    email=email,
                    username=username,
                    password=password
                )
                user.set_password(password)
                user.save()
            else:
                user = User.objects.get(email=email)
            # user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему!")
            return redirect("/")  # Перенаправляем на главную
        else:
            is_exist = User.objects.filter(username=email).exists()
            # user = form.get_user()
            print(is_exist)
            if is_exist:
                user = User.objects.get(username=email)
                login(request, user)
                messages.success(request, "Вы успешно вошли в систему!")
                return redirect("/")

        form = LoginForm()
        return render(request, "registration/login.html", {"form": form})
     # если это GET-запрос
    form = LoginForm()  # Здесь создаем форму для отображения на странице
    return render (request, "registration/login.html", {"form": form})