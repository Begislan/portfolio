from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from django.conf import settings
from urllib.parse import urlencode
from weasyprint import HTML
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template

from .models import Portfolio, CustomUser

import qrcode
import base64
import time
from io import BytesIO


def generate_qr_base64(data: str) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=3,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


@login_required
def portfolio_pdf(request, pk):
    user = CustomUser.objects.get(pk=pk)
    portfolios = Portfolio.objects.filter(user=user, active=True)

    if not portfolios.exists():
        return HttpResponse("No portfolios found", status=404)

    change_page_id = request.GET.get('change_page')

    if change_page_id:
        try:
            change_page = portfolios.get(id=change_page_id)
        except Portfolio.DoesNotExist:
            change_page = portfolios.first()
    else:
        change_page = portfolios.first()

    # Реконструируем текущий URL PDF
    base_url = reverse('portfolio_pdf', kwargs={'pk': user.pk})

    query = {}
    if change_page:
        query['change_page'] = change_page.id

    pdf_url = request.build_absolute_uri(base_url + ('?' + urlencode(query) if query else ''))

    qr_code_base64 = generate_qr_base64(pdf_url)

    template = get_template('core/portfolio_pdf.html')
    html = template.render({
        "user": user,
        "portfolios": portfolios,
        "change_page": change_page,
        "qr_code_base64": qr_code_base64,
        "pdf_url": pdf_url
    }, request)

    pdf_file = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')

    filename = f"portfolio_{user.username}"
    if change_page and change_page.menu:
        filename += f"_{change_page.menu}"
    elif change_page:
        filename += f"_{change_page.id}"

    response['Content-Disposition'] = f'filename="{filename}.pdf"'
    return response



def core(request):
    users = CustomUser.objects.all()
    portfolios = Portfolio.objects.all()
    context = {
        'users': users.count(),
        'portfolios': portfolios.count(),
    }
    return render(request, 'core/index.html', context)


@login_required
def user(request, username):
    """
    Публичный профиль — виден только самому владельцу или администратору.
    """
    profile_user = get_object_or_404(CustomUser, username=username)

    # Проверка доступа
    if request.user != profile_user and not request.user.is_superuser:
        return redirect('core')

    portfolios = Portfolio.objects.filter(user=profile_user, active=True)

    change_page = request.GET.get('change_page')
    if change_page:
        try:
            change_page = portfolios.get(id=change_page)
        except Portfolio.DoesNotExist:
            change_page = portfolios.first()
    else:
        change_page = portfolios.first()

    context = {
        'user': profile_user,
        'portfolios': portfolios,
        'change_page': change_page,
    }
    return render(request, 'core/user.html', context)


@login_required
def list_portfolios(request):
    """
    Список всех портфолио — только для администратора.
    """
    if not request.user.is_superuser:
        return redirect('core')

    query = request.GET.get('q', '')
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

    paginator = Paginator(data, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'core/list_portfolios.html', context)


def delete_user(request, username):
    if not request.user.is_superuser:
        return redirect('core')
    portfolios = Portfolio.objects.filter(user__username=username)
    if portfolios.exists():
        portfolios.delete()
    return redirect('list_portfolios')


