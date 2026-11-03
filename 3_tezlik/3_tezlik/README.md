# 3-to'plam: tezlik

## Tekshiruv natijasi (03.11, 15:55)
| Narsa | Holat |
|---|---|
| gzip siqish (HTML, CSS, JS) | Ishlaydi, `.htaccess` kerak emas |
| Statik fayllar keshi | CSS/JS 30 kun, rasm 60 kun. Ishlaydi |
| WebP + srcset | `/_resp/` tizimi bor. Faqat `imagesLoaded` xatosi uni buzayotgan edi (app.js tuzatishi) |
| Bosh sahifa javobi | 1-so'rov **1 501 ms**, keyingilari 20-30 ms |
| reCAPTCHA | Har sahifada ~500 KB JS, forma ishlatilmasa ham |
| Jetour logosi | 7467×1216 px PNG, ekranda 118 px |

Asosiy sekinlik **Passenger sovuq starti**: saytga bir necha daqiqa so'rov kelmasa, cPanel Python ilovani to'xtatadi. Keyingi kelgan foydalanuvchi va Googlebot 1.5 s kutadi. 508 xatosi ham ko'pincha shu qayta ishga tushish paytida chiqadi.

---

## 1. Ilovani "issiq" saqlash (cron), 10 daqiqa ish
**cPanel > Cron Jobs > Add New Cron Job**
- Common Settings: `Once Per Five Minutes (*/5 * * * *)`
- Command:
```
curl -s -o /dev/null -A "Autoliga-warmup" https://autoliga.uz/ ; curl -s -o /dev/null -A "Autoliga-warmup" https://autoliga.uz/ru/
```
Eslatmalar:
- Har 4-5 daqiqada 2 ta so'rov yuboriladi. Hosting limiti uchun bu juda kam yuk.
- Bu so'rovlar Google Analytics va Metrika'ga tushmaydi, chunki JS ishlamaydi.
- Hosting support'dan `PassengerPoolIdleTime` va `PassengerMinInstances` ni so'rash mumkin. Ular ruxsat bersa, cron kerak bo'lmaydi.

**Tekshirish** (10 daqiqa kutib, keyin):
```
curl -o /dev/null -s -w "%{time_starttransfer}\n" https://autoliga.uz/
```
Natija 0.3 dan kam bo'lishi kerak (hozir sovuq holatda 1.5).

---

## 2. reCAPTCHA'ni kechiktirib yuklash, 1-2 soat
Fayllar: `static/js/recaptcha-lazy.js`, `templates/forma_yuborish_misol.js`

1. `recaptcha-lazy.js` ni `static/js/` ga qo'ying.
2. Shablondagi (base.html yoki footer) qatorni o'chiring:
   `<script src="https://www.google.com/recaptcha/api.js?render=..." async defer></script>`
3. O'rniga qo'ying (RECAPTCHA_SITE_KEY e'lon qilingan inline skriptdan KEYIN):
   `<script src="{% static 'js/recaptcha-lazy.js' %}" defer></script>`
4. 3 ta formaning yuborish kodida `grecaptcha.ready(...)` ni `submitWithRecaptcha(...)` ga almashtiring (`forma_yuborish_misol.js` ga qarang).
5. `collectstatic` va Restart.

Tekshirish:
- Sahifa ochilganda DevTools > Network'da `recaptcha` so'rovi yo'q.
- Forma maydoniga bosilganda `api.js` yuklanadi.
- Sharh, aloqa va test-drayv formasi yuborilsa, serverda token tekshiruvi o'tadi (admin'da yangi yozuv paydo bo'ladi).

---

## 3. Jetour logosi, 10 daqiqa
`/media/categories/icons/Jetour_logo.svg.png` 7467×1216 px. Admin > Brendlar > JETOUR'da ikonkani boshqa brendlar bilan bir o'lchamga keltiring: **240 px kenglik, PNG yoki SVG**.
Terminalda tez yo'l (asl faylning zaxirasi qoladi):
```
cd /home/autolig1/site/media/categories/icons
cp Jetour_logo.svg.png Jetour_logo.svg.png.bak
python -c "from PIL import Image; im=Image.open('Jetour_logo.svg.png'); im.thumbnail((240,240)); im.save('Jetour_logo.svg.png', optimize=True)"
```
`/_resp/` papkasida shu logoning eski versiyalari bo'lsa, ularni o'chiring, tizim qayta yaratadi.

---

## 4. app.js: imagesLoaded (dasturchiga avval aytilgan)
```js
imgLoad = imagesLoaded(content.querySelectorAll('img:not([loading="lazy"])')),
```

---

## Hammasidan keyin o'lchash
PageSpeed Insights (mobil): https://pagespeed.web.dev/analysis?url=https://autoliga.uz/
| Ko'rsatkich | Maqsad |
|---|---|
| LCP | < 2.5 s |
| TBT | < 300 ms |
| CLS | < 0.1 |
| Bosh sahifa rasmlari | < 1 MB (DevTools > Network > Img) |
| Sovuq javob (TTFB) | < 0.5 s |

Kerak emas (allaqachon ishlaydi): `.htaccess` gzip/kesh, rasmlarni WebP'ga o'girish skripti.
