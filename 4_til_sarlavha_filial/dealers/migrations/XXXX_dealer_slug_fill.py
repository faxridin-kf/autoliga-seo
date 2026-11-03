"""
Ma'lumot migratsiyasi: mavjud 3 filialga slug yozadi.

Tartib:
  1) models.py ga slug maydonini qo'shing
  2) python manage.py makemigrations dealers          -> 00NN_dealer_slug.py (maydon qo'shadi)
  3) Shu faylni dealers/migrations/ ga 00NN+1_dealer_slug_fill.py nomi bilan qo'ying
  4) Pastdagi dependencies'ga 2-qadamda yaratilgan migratsiya nomini yozing
  5) python manage.py migrate

ID'lar 03.11.2026 holatiga saytdan olingan:
  1 = Autoliga Yunusobod, 3 = Autoliga Olmaliq, 4 = Autoliga Samarqand
"""
from django.db import migrations

SLUGS = {
    1: "yunusobod",
    3: "olmaliq",
    4: "samarqand",
}


def fill(apps, schema_editor):
    Dealer = apps.get_model("dealers", "Dealer")   # <-- app va model nomini moslang
    for pk, slug in SLUGS.items():
        Dealer.objects.filter(pk=pk, slug__isnull=True).update(slug=slug)
    # Ro'yxatda yo'q filiallar (agar bo'lsa) uchun vaqtinchalik slug
    for d in Dealer.objects.filter(slug__isnull=True):
        d.slug = f"filial-{d.pk}"
        d.save(update_fields=["slug"])


def unfill(apps, schema_editor):
    Dealer = apps.get_model("dealers", "Dealer")
    Dealer.objects.update(slug=None)


class Migration(migrations.Migration):
    dependencies = [
        ("dealers", "00NN_dealer_slug"),   # <-- 2-qadamdagi migratsiya nomi
    ]
    operations = [migrations.RunPython(fill, unfill)]
