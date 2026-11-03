# 4-to'plam: til tugmasi, bo'sh sarlavhalar, title, filial URL'lari

Barcha belgilar (class, id, filial ID) 03.11.2026 da saytdan olingan.

## Oldindan bilish kerak
- 1-3 ishlar faqat shablon o'zgarishi: migratsiya yo'q, xavf past.
- 4-ish (filial slug) bazaga maydon qo'shadi, oldin zaxira oling.
- Har o'zgarishdan keyin: `collectstatic` (agar CSS o'zgarsa) va cPanel > Setup Python App > Restart.
- **Ma'lumotni tekshiring:** "Autoliga Olmaliq" filialining manzili sxemada "Toshkent viloyati, Piskent tumani" deb turibdi. Olmaliq Piskent tumanida emas. Admin'da manzilni to'g'rilang, aks holda Google xaritasi va schema chalkashadi.

## 1. Til tugmasi (30 daqiqa)
**Muammo:** ru va en sahifalardagi "O'zbek" havolasi `/set-language/?language=uz&next=...` ga olib boradi. Bu yo'l robots.txt'da yopiq, `rel="nofollow"` ham bor. Natijada crawler ru'dan uz'ga havola orqali o'ta olmaydi.
**Fayllar:** `core/templatetags/i18n_extra.py`, `templates/includes/lang_switcher.html`
1. `i18n_extra.py` ni `core/templatetags/` ga qo'ying.
2. Shablondagi `<nav class="language-switcher">...</nav>` blokini `{% include "includes/lang_switcher.html" %}` bilan almashtiring.
3. Shablonda `request` bo'lishi kerak: settings > TEMPLATES > context_processors ichida `django.template.context_processors.request`.

**Tekshirish:** https://autoliga.uz/ru/products/jetour-t1/ sahifa kodida O'zbek havolasi `href="/products/jetour-t1/"`. Bosganda uz sahifa ochiladi, keyin `/` ga kirganda ham uz qoladi.

## 2. Bo'sh sarlavhalar (20 daqiqa)
**Fayl:** `templates/sarlavhalar_ozgarish.html` (A qism)
3 ta teg: `#ht3dName` (h3), `#htmName` (h2), `#tmName` (h2), `<div>` ga o'zgaradi. JS id orqali ishlaydi, o'zgarmaydi.
```
grep -rn 'id="ht3dName"\|id="htmName"\|id="tmName"' templates/
grep -rnE "h[23]\.(ht3d-name|home-team-modal-name|team-modal-name)" static/css
```
**Tekshirish:** bosh sahifa va /team/ da jamoa a'zosini bosganda ism ko'rinadi. Sahifa kodida bo'sh `<h2>`/`<h3>` yo'q.

## 3. Bosh sahifa title (10 daqiqa)
**Fayl:** `templates/sarlavhalar_ozgarish.html` (B qism)
| Til | Title (= og:title) |
|---|---|
| uz | Jetour, Geely, Soueast, JAC rasmiy dileri Toshkentda \| AUTOLIGA |
| ru | Официальный дилер Jetour, Geely, Soueast, JAC в Ташкенте \| AUTOLIGA |
| en | Official Jetour, Geely, Soueast, JAC dealer in Tashkent \| AUTOLIGA |

Title admin'dagi SEO maydonidan olinsa, kodni emas, admin'ni o'zgartiring.

## 4. Filial URL'lari (1-2 soat)
**Fayllar:** `dealers/ozgarishlar.py`, `dealers/migrations/XXXX_dealer_slug_fill.py`
| Eski | Yangi |
|---|---|
| /dealers/1/ | /dealers/yunusobod/ |
| /dealers/3/ | /dealers/olmaliq/ |
| /dealers/4/ | /dealers/samarqand/ |
```
python manage.py makemigrations dealers
# XXXX_dealer_slug_fill.py ni nomlab, dependencies ni to'ldiring
python manage.py migrate
touch tmp/restart.txt
```
**Tekshirish:**
```
curl -sI https://autoliga.uz/dealers/1/     | grep -iE "^HTTP|^location"   # 301 -> /dealers/yunusobod/
curl -sI https://autoliga.uz/ru/dealers/4/  | grep -iE "^HTTP|^location"   # 301 -> /ru/dealers/samarqand/
curl -s https://autoliga.uz/sitemap.xml | grep -c "dealers/[0-9]"           # 0
```

## Keyin (SEO)
- GSC > URL Inspection: /dealers/yunusobod/, /dealers/samarqand/, /dealers/olmaliq/ uchun Request indexing.
- Google Business Profile va Yandex Business'dagi sayt havolasini filialning yangi URL'iga almashtirish.
