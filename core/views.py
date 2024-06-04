from django.shortcuts import render
from .models import Portfolio

# Create your views here.
def core(request):
    return render(request, 'core/index.html')

def user(request, username):
    portfolios = Portfolio.objects.get(user__username=username)
    print(username,portfolios)
    return render(request, 'core/user.html', {'portfolios': portfolios})
