# sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import CustomUser

class PortfolioSitemap(Sitemap):
    changefreq = 'Портфолио'
    priority = 1

    def items(self):
        return CustomUser.objects.all()

    def lastmod(self, obj):
        return obj.date_joined

    def location(self, obj):
        return obj.get_absolute_url()
