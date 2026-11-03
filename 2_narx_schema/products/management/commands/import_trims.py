"""
products/management/commands/import_trims.py
(products/management/__init__.py va products/management/commands/__init__.py bo'sh fayllar bo'lishi shart)

Eski matn maydonidagi narxlarni Trim jadvaliga AVTOMATIK ko'chiradi.
Misol matnlar:
    "COMFORT (386 500 000) PREMIUM(449 500 000)"
    "Comfort (253 500 000 soʻm) Luxury (273 000 000 soʻm)"
    "403 000 000 sum"                      -> bitta "Standart" komplektatsiya
    "Narx so'rang"                         -> o'tkazib yuboriladi

Quvvat ham shu usulda: "COMFORT (184 hp) PREMIUM (254 hp)" yoki "156 o.k."

Ishlatish:
    python manage.py import_trims            # faqat ko'rsatadi, bazaga yozmaydi
    python manage.py import_trims --apply    # bazaga yozadi

MOSLASH KERAK: OLD_PRICE_FIELD va OLD_POWER_FIELD (eski matn maydonlari nomi).
Eski maydonlarni hozircha O'CHIRMANG: hammasi tekshirilgach, alohida migratsiyada.
"""
import re

from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Product, Trim

OLD_PRICE_FIELD = "price"   # <-- moslang
OLD_POWER_FIELD = "power"   # <-- moslang (yo'q bo'lsa None qiling)

PAIR_RE = re.compile(r"([A-Za-zА-Яа-яЁё][\w\s\-]{1,25}?)\s*\(\s*([\d\s .,]+)[^)]*\)")
NUM_RE = re.compile(r"\d[\d\s .,]*\d|\d")


def to_int(s):
    digits = re.sub(r"[^\d]", "", s or "")
    return int(digits) if digits else None


def parse(text, min_value):
    """Matndan [(komplektatsiya, raqam), ...] ro'yxat qaytaradi."""
    text = (text or "").strip()
    if not text:
        return []
    pairs = [(n.strip().title(), to_int(v)) for n, v in PAIR_RE.findall(text)]
    pairs = [(n, v) for n, v in pairs if v and v >= min_value]
    if pairs:
        return pairs
    nums = [to_int(m) for m in NUM_RE.findall(text)]
    nums = [n for n in nums if n and n >= min_value]
    return [("Standart", nums[0])] if nums else []


class Command(BaseCommand):
    help = "Eski matn narxlarini Trim modeliga ko'chiradi"

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Bazaga yozish")

    def handle(self, *args, **opts):
        apply = opts["apply"]
        created, skipped = 0, []
        with transaction.atomic():
            for p in Product.objects.all().order_by("pk"):
                if p.trims.exists():
                    self.stdout.write(f"= {p}: Trim allaqachon bor, o'tkazildi")
                    continue
                prices = parse(getattr(p, OLD_PRICE_FIELD, ""), 1_000_000)
                powers = dict(parse(getattr(p, OLD_POWER_FIELD, ""), 30)) if OLD_POWER_FIELD else {}
                if not prices:
                    skipped.append(str(p))
                    self.stdout.write(self.style.WARNING(f"- {p}: narx topilmadi -> qo'lda kiriting"))
                    continue
                for i, (name, price) in enumerate(prices):
                    hp = powers.get(name) or (list(powers.values())[i] if i < len(powers) else None)
                    self.stdout.write(f"+ {p}: {name} = {price:,} so'm, {hp or '-'} o.k.".replace(",", " "))
                    if apply:
                        Trim.objects.create(product=p, name=name, price=price, power_hp=hp, order=i)
                    created += 1
            if not apply:
                transaction.set_rollback(True)

        mode = "YOZILDI" if apply else "SINOV (bazaga yozilmadi, --apply qo'shing)"
        self.stdout.write(self.style.SUCCESS(f"\n{mode}: {created} ta komplektatsiya"))
        if skipped:
            self.stdout.write(self.style.WARNING("Narxsiz modellar: " + ", ".join(skipped)))
