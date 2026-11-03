"""
products/admin.py ga QO'SHILADI.

Mavjud ProductAdmin va BrandAdmin bo'lsa, ularga faqat `inlines` qatorini qo'shing.
Agar inlines allaqachon bor bo'lsa: inlines = [ESKI..., TrimInline, ProductFAQInline]
Agar modeltranslation ishlatilsa, TranslationTabularInline dan meros oling.
"""
from django.contrib import admin

from .models import Trim, FAQ


class TrimInline(admin.TabularInline):
    model = Trim
    extra = 1
    fields = ("name", "price", "power_hp", "fuel_l100", "order")


class ProductFAQInline(admin.StackedInline):
    model = FAQ
    fk_name = "product"
    extra = 1
    fields = ("question", "answer", "order")


class BrandFAQInline(admin.StackedInline):
    model = FAQ
    fk_name = "brand"
    extra = 1
    fields = ("question", "answer", "order")


# --- Mavjud klasslarga qo'shing ---
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [TrimInline, ProductFAQInline]
#
# class BrandAdmin(admin.ModelAdmin):
#     inlines = [BrandFAQInline]
