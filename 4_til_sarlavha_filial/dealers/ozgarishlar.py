"""
FILIAL URL'LARI: /dealers/1/  ->  /dealers/yunusobod/

Bu fayl alohida ishlatilmaydi. 3 ta joyga qo'shiladi: models.py, urls.py, views.py.
Keyin migratsiya: dealers/migrations/XXXX_dealer_slug_fill.py (alohida fayl).

Natija:
  /dealers/yunusobod/   /ru/dealers/yunusobod/   /en/dealers/yunusobod/
  /dealers/samarqand/   ...
  /dealers/olmaliq/     ...
  Eski /dealers/1/, /dealers/3/, /dealers/4/  ->  301 yangi manzilga (uchala tilda).
"""

# ============================================================
# 1) dealers/models.py  ->  Dealer klassiga
# ============================================================
from django.db import models
from django.urls import reverse


class Dealer(models.Model):
    # ... mavjud maydonlar ...
    slug = models.SlugField("URL nomi", max_length=80, unique=True, null=True, blank=True,
                            help_text="Lotin, kichik harf: yunusobod, samarqand, olmaliq")

    def get_absolute_url(self):
        # sitemap, menyu, AutoDealer schema shu yerdan oladi
        if self.slug:
            return reverse("dealer_detail", kwargs={"slug": self.slug})
        return reverse("dealer_detail_id", kwargs={"pk": self.pk})


# ============================================================
# 2) dealers/views.py
# ============================================================
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView


class DealerDetailView(DetailView):          # mavjud view bo'lsa, faqat slug qatorlarini qo'shing
    model = Dealer
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "dealers/detail.html"    # <-- mavjud shablon nomi


def dealer_by_id_redirect(request, pk):
    """Eski raqamli URL -> slug URL, 301. Til prefiksi saqlanadi (reverse joriy tilni oladi)."""
    dealer = get_object_or_404(Dealer, pk=pk)
    if not dealer.slug:
        return DealerDetailView.as_view(pk_url_kwarg="pk", slug_url_kwarg=None)(request, pk=pk)
    return redirect(dealer.get_absolute_url(), permanent=True)


# ============================================================
# 3) dealers/urls.py  (i18n_patterns ICHIDA, hozirgi dealers yo'llari turgan joyda)
# ============================================================
from django.urls import path

urlpatterns = [
    path("dealers/<int:pk>/", dealer_by_id_redirect, name="dealer_detail_id"),   # int birinchi
    path("dealers/<slug:slug>/", DealerDetailView.as_view(), name="dealer_detail"),
]
# Eslatma: shablonlarda {% url 'dealer_detail' dealer.pk %} kabi yozilgan bo'lsa,
# {{ dealer.get_absolute_url }} ga almashtiring.
#   grep -rn "dealer_detail\|dealers/{{" templates/
