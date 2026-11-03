# 1-to'plam: robots.txt, sitemap, redirect

## Oldindan bilish kerak
- Model va app nomlari (`products`, `news`, `dealers`, `Product`, `Brand`...) namuna. `core/sitemaps.py` boshidagi importlarni loyihaga moslang.
- `STATIC_PAGES` dagi nomlar urls.py dagi `name=` qiymatlari bilan bir xil bo'lishi kerak, aks holda `NoReverseMatch` xatosi chiqadi.
- Server Nginx bo'lsa `nginx/autoliga.conf`, Apache/cPanel bo'lsa `nginx/.htaccess`. Ikkalasi emas.
- `sitemap.xml` va `robots.txt` yo'llari `i18n_patterns` ichiga YOZILMAYDI.
- Admin > Sites da domen `example.com` bo'lsa, sitemap'dagi barcha URL noto'g'ri chiqadi. `autoliga.uz` qiling.

## Fayllar
| Fayl | Qayerga |
|---|---|
| `robots.txt` | Faqat static orqali berilsa. Django view ishlatilsa kerak emas |
| `core/sitemaps.py` | `core/sitemaps.py` (yangi fayl) |
| `core/urls_qoshimcha.py` | Ichidagi 2 ta `path(...)` ni asosiy `urls.py` ga |
| `core/settings_qoshimcha.py` | Qiymatlarni `settings.py` ga |
| `nginx/autoliga.conf` | `/etc/nginx/sites-available/autoliga.conf` |
| `nginx/.htaccess` | Faqat Apache/cPanel |

## Tartib
1. Staging'da: settings, sitemaps.py, urls o'zgarishlari, keyin `python manage.py migrate`.
2. Admin > Sites: domain = `autoliga.uz`.
3. `https://<staging>/sitemap.xml` ochiladi, xato yo'q.
4. Production'ga chiqarish, keyin `sudo certbot --nginx -d autoliga.uz -d www.autoliga.uz`.
5. Nginx konfigni almashtirish: `sudo nginx -t && sudo systemctl reload nginx`.
6. Kesh tozalash (Django, CDN).

## Tekshirish
```
curl -s https://autoliga.uz/robots.txt
curl -I http://autoliga.uz/                 # 301 -> https://autoliga.uz/
curl -I http://www.autoliga.uz/news/        # 301 -> https://autoliga.uz/news/
curl -I https://www.autoliga.uz/news/       # 301 -> https://autoliga.uz/news/
curl -s https://autoliga.uz/sitemap.xml | grep -c "<url>"
curl -s https://autoliga.uz/sitemap.xml | grep -c "<lastmod>"   # <url> soni bilan teng
curl -s https://autoliga.uz/sitemap.xml | grep -c "example.com" # 0
curl -sI -H "Accept-Encoding: gzip" https://autoliga.uz/ | grep -i content-encoding   # gzip
```

## Keyin (SEO)
- Google Search Console > Sitemaps: `https://autoliga.uz/sitemap.xml` qayta yuborish.
- Yandex.Webmaster > Индексирование > Файлы Sitemap: qayta yuborish.
- Yandex.Webmaster > Инструменты > Анализ robots.txt: `/admin/` "запрещён" ekanini tekshirish.
