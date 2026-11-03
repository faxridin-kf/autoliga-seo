"""
settings.py ga QO'SHILADI yoki mavjud qiymatlar shunga almashtiriladi.
"""

# 1) Sitemap ishlashi uchun
INSTALLED_APPS += [
    "django.contrib.sites",       # allaqachon bo'lsa qo'shmang
    "django.contrib.sitemaps",
]
SITE_ID = 1
# Keyin: python manage.py migrate
# Admin > Sites > domain = autoliga.uz, name = Autoliga  (example.com bo'lmasin!)

# 2) Tillar (sitemap hreflang shu ro'yxatdan olinadi)
LANGUAGE_CODE = "uz"
LANGUAGES = [
    ("uz", "O'zbek"),
    ("ru", "Русский"),
    ("en", "English"),
]

# 3) Domen va https
PREPEND_WWW = False
APPEND_SLASH = True
SECURE_SSL_REDIRECT = True                       # Nginx ham redirect qiladi, bu zaxira
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = ["autoliga.uz", "www.autoliga.uz"]
CSRF_TRUSTED_ORIGINS = ["https://autoliga.uz"]

# HSTS: hammasi ishlagani tasdiqlangandan KEYIN yoqing (1 haftadan so'ng)
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
