from django.shortcuts import render, redirect
from core.models import Portfolio, CustomUser
from django.contrib.auth.decorators import login_required
from .forms import PortfolioForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserUpdateForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash


@login_required
def admin_core(request):
    user = request.user
    portfolio = Portfolio.objects.filter(user=user)

    context = {
        "user": user,
        "portfolio": portfolio,
    }
    return render(request, 'adm/adm_core.html', context)


@login_required
def admin_portfolio_detail(request, id):
    user = request.user
    portfolio = Portfolio.objects.filter(user=user)
    detail_data = Portfolio.objects.get(id=id)
    context = {
        "user": user,
        "portfolio": portfolio,
        "detail_data": detail_data
    }
    return render(request, 'adm/admin_detail.html', context)


@login_required
def portfolio_create_view(request):
    user = request.user
    portfolio = Portfolio.objects.filter(user=user)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user  # Назначаем текущего пользователя
            portfolio.save()
            return redirect('admin_core')  # Поменяйте на нужный URL
    else:
        form = PortfolioForm()

    context = {
        'form': form,
        'portfolio': portfolio
    }
    return render(request, 'adm/admin_create.html', context)


@login_required
def portfolio_update_view(request, pk):
    user = request.user
    portfolio = Portfolio.objects.filter(user=user)
    portfolios = get_object_or_404(Portfolio, pk=pk, user=request.user)

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolios)
        if form.is_valid():
            form.save()
            return redirect('admin_core')  # Поменяйте на нужный URL
    else:
        form = PortfolioForm(instance=portfolios)

    context = {
        'form': form,
        'portfolio': portfolio
    }
    return render(request, 'adm/admin_update.html', context)


@login_required
def portfolio_delete_view(request, pk):
    user = request.user
    portfolio = Portfolio.objects.filter(user=user)
    # Получаем объект Portfolio или возвращаем 404, если объект не найден
    portfolios = get_object_or_404(Portfolio, pk=pk, user=request.user)

    if request.method == 'POST':
        # Удаление объекта после подтверждения пользователя
        portfolios.delete()
        return redirect('admin_core')  # Поменяйте на нужный URL

    context = {
        'portfolios': portfolios,
        'portfolio': portfolio
    }
    return render(request, 'adm/admin_delete.html', context)


@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
        'portfolio': Portfolio.objects.filter(user=user),
    }
    return render(request, 'adm/profile.html', context)


@login_required
def update_profile(request):
    user = request.user
    portfolio = Portfolio.objects.filter(user=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'adm/update_profile.html', {'form': form, 'user': user, "portfolio": portfolio})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'adm/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)  # Обновляем сессию, чтобы пользователь не был разлогинен
        return super().form_valid(form)


