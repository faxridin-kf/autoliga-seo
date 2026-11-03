"""
core/templatetags/seo_schema.py  (yangi fayl)
core/templatetags/__init__.py bo'lishi shart (bo'sh fayl).

JSON-LD Python'da json.dumps bilan yasaladi: qo'shtirnoq yoki yangi qator
matnni buzmaydi (shablonda qo'lda yozilgan JSON ko'p xato beradi).

Shablonda:
    {% load seo_schema %}
    {% car_schema product %}
    {% faq_schema product.faqs.all %}
    <meta name="description" content="{% product_meta_description product %}">
    {{ trim.price|som }} so'm

MOSLASH KERAK: quyidagi FIELD_* qiymatlari (Product va Brand maydon nomlari).
"""
import json

from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

register = template.Library()

SITE = "https://autoliga.uz"

# ---- Loyihaga moslang ----
FIELD_NAME = "name"            # Product.name  -> "T1"  yoki "Jetour T1"
FIELD_BRAND = "brand"          # Product.brand (ForeignKey)
FIELD_YEAR = "year"            # Product.year  (yo'q bo'lsa e'tiborsiz)
FIELD_DESC = "seo_description" # bo'sh bo'lsa FIELD_DESC_FALLBACK olinadi
FIELD_DESC_FALLBACK = "description"
FIELD_IMAGES = "images"        # related_name (ProductImage), har birida .image
FIELD_MAIN_IMAGE = "main_image"
# --------------------------

CITIES = {
    "uz": "Toshkent, Samarqand, Olmaliq",
    "ru": "Ташкент, Самарканд, Алмалык",
    "en": "Tashkent, Samarkand, Almalyk",
}


def _ld(data):
    js = json.dumps(data, ensure_ascii=False, indent=None)
    js = js.replace("</", "<\\/")  # </script> xavfsizligi
    return mark_safe(f'<script type="application/ld+json">{js}</script>')


def _full_name(p):
    name = getattr(p, FIELD_NAME, "") or ""
    brand = getattr(p, FIELD_BRAND, None)
    bname = getattr(brand, "name", "") if brand else ""
    if bname and not name.lower().startswith(bname.lower()):
        return f"{bname} {name}".strip(), bname
    return name, bname


def _abs(url):
    if not url:
        return None
    return url if url.startswith("http") else SITE + url


def _images(p):
    out = []
    main = getattr(p, FIELD_MAIN_IMAGE, None)
    if main:
        try:
            out.append(_abs(main.url))
        except ValueError:
            pass
    rel = getattr(p, FIELD_IMAGES, None)
    if rel is not None:
        for im in rel.all()[:5]:
            f = getattr(im, "image", None)
            if f:
                try:
                    out.append(_abs(f.url))
                except ValueError:
                    pass
    return list(dict.fromkeys(out))[:6]


@register.filter
def som(value):
    """386500000 -> '386 500 000'"""
    if value in (None, ""):
        return ""
    try:
        return f"{int(value):,}".replace(",", " ")
    except (TypeError, ValueError):
        return value


@register.simple_tag
def product_meta_description(product):
    lang = (get_language() or "uz")[:2]
    full, _ = _full_name(product)
    price = getattr(product, "price_from", None)
    hp = getattr(product, "power_max", None)
    cities = CITIES.get(lang, CITIES["uz"])
    if lang == "ru":
        if price:
            s = f"{full}: цена от {som(price)} сум" + (f", {hp} л.с" if hp else "")
            return f"{s}. Кредит и тест-драйв. Официальный дилер Autoliga: {cities}."
        return f"{full}: узнайте цену, кредит и тест-драйв. Официальный дилер Autoliga: {cities}."
    if lang == "en":
        if price:
            s = f"{full}: price from {som(price)} UZS" + (f", {hp} hp" if hp else "")
            return f"{s}. Financing and test drive. Official dealer Autoliga: {cities}."
        return f"{full}: ask for price, financing and test drive. Official dealer Autoliga: {cities}."
    if price:
        s = f"{full}: narxi {som(price)} so'mdan" + (f", {hp} o.k" if hp else "")
        return f"{s}. Kredit va test-drayv. Rasmiy diler Autoliga: {cities}."
    return f"{full}: narxini so'rang, kredit va test-drayv. Rasmiy diler Autoliga: {cities}."


@register.simple_tag(takes_context=True)
def car_schema(context, product):
    request = context.get("request")
    url = request.build_absolute_uri(request.path) if request else SITE
    full, bname = _full_name(product)
    desc = getattr(product, FIELD_DESC, "") or getattr(product, FIELD_DESC_FALLBACK, "") or ""
    desc = " ".join(strip_tags(desc).split())[:300] or product_meta_description(product)

    data = {
        "@context": "https://schema.org",
        "@type": "Car",
        "@id": url + "#car",
        "name": full,
        "url": url,
        "description": desc,
        "itemCondition": "https://schema.org/NewCondition",
    }
    if bname:
        data["brand"] = {"@type": "Brand", "name": bname}
        data["manufacturer"] = {"@type": "Organization", "name": bname}
    model = getattr(product, FIELD_NAME, None)
    if model:
        data["model"] = model
    year = getattr(product, FIELD_YEAR, None)
    if year:
        data["vehicleModelDate"] = str(year)
    imgs = _images(product)
    if imgs:
        data["image"] = imgs
    hp = getattr(product, "power_max", None)
    if hp:
        data["vehicleEngine"] = {
            "@type": "EngineSpecification",
            "enginePower": {"@type": "QuantitativeValue", "value": hp, "unitCode": "BHP"},
        }

    low = getattr(product, "price_from", None)
    high = getattr(product, "price_to", None)
    if low:  # narx bo'lmasa offers umuman chiqmaydi (0 yoki bo'sh narx Google'da xato)
        data["offers"] = {
            "@type": "AggregateOffer",
            "priceCurrency": "UZS",
            "lowPrice": low,
            "highPrice": high or low,
            "offerCount": getattr(product, "priced_trims_count", 1) or 1,
            "availability": "https://schema.org/InStock",
            "url": url,
            "seller": {"@type": "AutoDealer", "name": "Autoliga", "url": SITE + "/"},
        }
    return _ld(data)


@register.simple_tag
def faq_schema(faqs):
    items = [
        {
            "@type": "Question",
            "name": " ".join(strip_tags(f.question).split()),
            "acceptedAnswer": {"@type": "Answer", "text": " ".join(strip_tags(f.answer).split())},
        }
        for f in faqs
        if f.question and f.answer
    ]
    if not items:
        return ""
    return _ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items})
