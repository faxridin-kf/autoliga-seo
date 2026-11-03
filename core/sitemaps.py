"""
autoliga.uz sitemap.

Joylashuvi: core/sitemaps.py
Nima qiladi:
  - har bir URL'ga lastmod qo'yadi (statik sahifalarga ham)
  - uz / ru / en versiyalarini hreflang (xhtml:link) bilan chiqaradi
  - faqat faol mahsulot, brend, filial va MATNI BOR yangiliklarni qo'shadi
    (matnsiz yangilik noindex, sitemap'da bo'lmasligi kerak)

MOSLASH KERAK (loyihadagi haqiqiy nomlarga):
  - import qatorlaridagi app va model nomlari
  - STATIC_PAGES dagi url name'lar (urls.py dagi name=... qiymatlari)
  - NEWS_BODY_FIELD: yangilik matni saqlanadigan maydon nomi
"""
from datetime import datetime, timezone as dt_tz

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils.html import strip_tags

from products.models import Product, Brand   # <-- moslang
from news.models import News                 # <-- moslang
from dealers.models import Dealer            # <-- moslang

# Statik sahifalar matni o'zgarsa shu sanani yangilang
STATIC_UPDATED = datetime(2026, 11, 3, tzinfo=dt_tz.utc)

# url name : priority
STATIC_PAGES = {
    "home": 1.0,
    "products": 0.9,
    "dealers": 0.8,
    "test_drive": 0.7,
    "contact": 0.7,
    "news": 0.6,
    "team": 0.4,
}

NEWS_BODY_FIELD = "body"        # <-- moslang (masalan: "content", "text")
NEWS_MIN_WORDS = 80             # news/detail.html dagi noindex chegarasi bilan bir xil


def _active(qs):
    """is_active yoki is_published maydoni bo'lsa, faqat faollarini qoldiradi."""
    fields = {f.name for f in qs.model._meta.get_fields()}
    if "is_active" in fields:
        qs = qs.filter(is_active=True)
    if "is_published" in fields:
        qs = qs.filter(is_published=True)
    return qs


def _lastmod(obj):
    for name in ("updated_at", "modified", "updated", "created_at", "created"):
        value = getattr(obj, name, None)
        if value:
            return value
    return STATIC_UPDATED


class I18nSitemap(Sitemap):
    """uz, ru, en uchun alohida URL va hreflang. settings.LANGUAGES dan o'qiydi."""
    i18n = True
    alternates = True
    x_default = True
    protocol = "https"

    def lastmod(self, obj):
        return _lastmod(obj)


class StaticSitemap(I18nSitemap):
    changefreq = "monthly"

    def items(self):
        return list(STATIC_PAGES.keys())

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return STATIC_PAGES[item]

    def lastmod(self, item):
        return STATIC_UPDATED


class BrandSitemap(I18nSitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return _active(Brand.objects.all()).order_by("pk")


class ProductSitemap(I18nSitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return _active(Product.objects.all()).order_by("pk")


class DealerSitemap(I18nSitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return _active(Dealer.objects.all()).order_by("pk")


class NewsSitemap(I18nSitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        qs = _active(News.objects.all()).order_by("-pk")
        result = []
        for n in qs:
            text = getattr(n, NEWS_BODY_FIELD, "") or ""
            if len(strip_tags(text).split()) >= NEWS_MIN_WORDS:
                result.append(n)
        return result


SITEMAPS = {
    "static": StaticSitemap,
    "brands": BrandSitemap,
    "products": ProductSitemap,
    "dealers": DealerSitemap,
    "news": NewsSitemap,
}
