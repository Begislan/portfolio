from django.shortcuts import render, redirect
from .models import Portfolio, CustomUser


# Create your views here.
def core(request):
    return render(request, 'core/index.html')

def user(request, username):
    portfolios = Portfolio.objects.filter(user__username=username, active=True)
    user = []
    if portfolios.exists():
        user = portfolios[0].user
    else:
        return redirect('index')
    change_page = request.GET.get('change_page')
    if change_page:
        change_page = portfolios.get(id=change_page)
    else:
        change_page = portfolios.first()

    print(username,portfolios)
    context = {
        'user': user,
        'portfolios': portfolios,
        'change_page': change_page
    }
    return render(request, 'core/user.html', context)


def list_portfolios(request):
    port = Portfolio.objects.all()
    return render(request, 'core/list_portfolios.html', {'port': port})

