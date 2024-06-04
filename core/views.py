from django.shortcuts import render, redirect
from .models import Portfolio

# Create your views here.
def core(request):
    return render(request, 'core/index.html')

def user(request, username):
    portfolios = Portfolio.objects.filter(user__username=username)
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
