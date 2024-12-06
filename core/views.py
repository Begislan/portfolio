from django.shortcuts import render, redirect
from .models import Portfolio, CustomUser
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def core(request):
    return render(request, 'core/index.html')

def user(request, username):
    portfolios = Portfolio.objects.filter(user__username=username, active=True)
    user = []
    if portfolios.exists():
        user = portfolios[0].user
    else:
        return redirect('core')
    change_page = request.GET.get('change_page')
    if change_page:
        change_page = portfolios.get(id=change_page)
    else:
        change_page = portfolios.first()
    context = {
        'user': user,
        'portfolios': portfolios,
        'change_page': change_page
    }
    return render(request, 'core/user.html', context)

@login_required
def list_portfolios(request):
    query = request.GET.get('q', '')  # Получаем запрос из строки поиска
    port = Portfolio.objects.filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(user__username__icontains=query)
    )

    data = []
    ids = []
    for i in port:
        if i.user.id not in ids:
            data.append(i)
            ids.append(i.user.id)

    paginator = Paginator(data, 10)  # Пагинация с 10 портфолио на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,  # Передаём строку поиска в шаблон
    }
    return render(request, 'core/list_portfolios.html', context)


def delete_user(request, username):
    portfolios = Portfolio.objects.filter(user__username=username)
    if portfolios.exists():
        portfolios.delete()
        return redirect('list_portfolios')

