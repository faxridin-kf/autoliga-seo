"""
Asosiy urls.py (loyiha papkasidagi, masalan config/urls.py) ga QO'SHILADI.
Bu fayl alohida ishlatilmaydi: ichidagi qatorlarni ko'chiring.

MUHIM: sitemap.xml va robots.txt i18n_patterns(...) ICHIGA emas,
oddiy urlpatterns ga yoziladi. Aks holda /ru/sitemap.xml paydo bo'ladi.
"""
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.cache import cache_page

from core.sitemaps import SITEMAPS

ROBOTS_TXT = """User-agent: *
Disallow: /admin/
Disallow: /api/
Disallow: /captcha/
Disallow: /set-language/
Disallow: /*?utm_
Disallow: /*&utm_
Allow: /

Clean-param: utm_source&utm_medium&utm_campaign&utm_content&utm_term&fbclid&yclid&gclid

Sitemap: https://autoliga.uz/sitemap.xml
"""


def robots_txt(request):
    return HttpResponse(ROBOTS_TXT, content_type="text/plain; charset=utf-8")


# --- shu ikki qatorni mavjud urlpatterns ro'yxatiga qo'shing ---
urlpatterns = [
    path("robots.txt", robots_txt, name="robots_txt"),
    path(
        "sitemap.xml",
        cache_page(60 * 60)(sitemap),          # 1 soat kesh
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

# Eslatma: agar robots.txt hozir Nginx yoki static fayl orqali berilayotgan bo'lsa,
# bitta joyda qoldiring: yo shu view, yo robots.txt fayli (ikkalasi emas).
