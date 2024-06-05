from django.shortcuts import render

def admin_core(request):
    return render(request, 'adm/adm_core.html')