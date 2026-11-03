# 2-to'plam: narx maydonlari, Car schema, FAQ schema

## Natija
- Narx endi raqam: `386 500 000 so'm`, xom `COMFORT (386 500 000)...` matni yo'qoladi.
- Meta description: `Jetour T1: narxi 386 500 000 so'mdan, 254 o.k. Kredit va test-drayv...` (uz/ru/en).
- Car JSON-LD'da `offers` (UZS, lowPrice/highPrice) va `vehicleEngine` paydo bo'ladi.
- Model va brend sahifalarida FAQPage schema.

## Oldindan bilish kerak
- Model va maydon nomlari namuna. Moslash kerak bo'lgan joylar:
  - `core/templatetags/seo_schema.py` boshidagi `FIELD_*` qiymatlari
  - `products/management/commands/import_trims.py` dagi `OLD_PRICE_FIELD`, `OLD_POWER_FIELD`
- Migratsiya bazaga yangi jadval qo'shadi. Oldin zaxira: cPanel > Backup yoki `mysqldump`/`pg_dump`.
- Shared hosting (cPanel Python App): har o'zgarishdan keyin Setup Python App > Restart.
- `templatetags` va `management/commands` papkalarida bo'sh `__init__.py` bo'lishi shart.
- Eski narx maydonini hozircha O'CHIRMANG. Hammasi tekshirilgach keyin olib tashlanadi.

## Fayllar
| Fayl | Nima qilish |
|---|---|
| `products/models_qoshimcha.py` | `Trim`, `FAQ` ni models.py ga ko'chirish, `Product` ga `ProductPriceMixin` qo'shish |
| `products/admin_qoshimcha.py` | Inline'larni admin.py ga qo'shish |
| `products/management/commands/import_trims.py` | Yangi fayl, eski narxlarni avtomatik ko'chiradi |
| `core/templatetags/seo_schema.py` | Yangi fayl: `som`, `car_schema`, `faq_schema`, `product_meta_description` |
| `templates/includes/faq.html` | Yangi fayl |
| `templates/products/detail_qoshimcha.html` | detail.html dagi 5 ta o'zgarish (fayl almashtirilmaydi) |

## Tartib
```
# 1. Kod qo'shilgandan keyin
python manage.py makemigrations products
python manage.py migrate

# 2. Narxlarni ko'chirish: avval sinov, natijani ko'rib chiqing
python manage.py import_trims
python manage.py import_trims --apply

# 3. Statik fayllar va restart
python manage.py collectstatic --noinput
touch tmp/restart.txt     # yoki cPanel > Setup Python App > Restart
```
4. Admin'da har modelni ochib komplektatsiyalarni tekshirish (16 model, 20-30 daqiqa). Narxi yo'q modellar "Narxini so'rang" bo'lib qoladi.
5. FAQ: model sahifadagi mavjud savollarni admin'dagi FAQ'ga ko'chirish. Brend FAQ matnini marketing beradi (har brendga 5 ta).
6. Shablonlarda eski narx matni chiqadigan joylarni almashtirish: model sahifasi, bosh sahifa slayderi, katalog va brend kartochkalari.

## Tekshirish
- https://autoliga.uz/products/jetour-t1/ sahifa kodida (Ctrl+U):
  - `<meta name="description" content="Jetour T1: narxi 386 500 000 so'mdan, 254 o.k. ...">`
  - `"@type": "Car"` ichida `"offers"`, `"lowPrice": 386500000`, `"priceCurrency": "UZS"`
  - `"@type": "FAQPage"` (FAQ to'ldirilgan bo'lsa)
  - `COMFORT (` matni yo'q
- https://search.google.com/test/rich-results : jetour-t1, monjaro, /brand/jetour/. Xato 0.
- https://validator.schema.org : xato 0.
- Narxi yo'q model (masalan JAC T8): `offers` chiqmaydi, description "narxini so'rang".

## Keyin (SEO)
- GSC > URL Inspection > Request indexing: 16 model sahifa.
- GSC > Enhancements: "Products"/"FAQ" hisobotlari 3-7 kunda paydo bo'ladi.
