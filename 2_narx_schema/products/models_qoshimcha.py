"""
products/models.py ga QO'SHILADI (alohida fayl sifatida ishlatilmaydi).

1) Trim va FAQ klasslarini models.py oxiriga ko'chiring.
2) ProductPriceMixin'ni mavjud Product klassiga qo'shing:
       class Product(ProductPriceMixin, models.Model):
3) Keyin:
       python manage.py makemigrations products
       python manage.py migrate
"""
from django.db import models


class Trim(models.Model):
    """Komplektatsiya: Comfort, Premium, Luxury... Narx RAQAM sifatida saqlanadi."""
    product = models.ForeignKey(
        "Product", related_name="trims", on_delete=models.CASCADE,
        verbose_name="Model",
    )
    name = models.CharField("Komplektatsiya", max_length=50)
    price = models.PositiveBigIntegerField("Narx, so'm", null=True, blank=True,
                                           help_text="Faqat raqam: 386500000")
    power_hp = models.PositiveIntegerField("Quvvat, o.k.", null=True, blank=True)
    fuel_l100 = models.DecimalField("Sarf, l/100 km", max_digits=4, decimal_places=1,
                                    null=True, blank=True)
    order = models.PositiveSmallIntegerField("Tartib", default=0)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Komplektatsiya"
        verbose_name_plural = "Komplektatsiyalar"

    def __str__(self):
        return f"{self.product} {self.name}"


class FAQ(models.Model):
    """Model yoki brend sahifasidagi savol-javob. Bittasini tanlang: product YOKI brand."""
    product = models.ForeignKey("Product", null=True, blank=True, related_name="faqs",
                                on_delete=models.CASCADE, verbose_name="Model")
    brand = models.ForeignKey("Brand", null=True, blank=True, related_name="faqs",
                              on_delete=models.CASCADE, verbose_name="Brend")
    question = models.CharField("Savol", max_length=255)
    answer = models.TextField("Javob")
    order = models.PositiveSmallIntegerField("Tartib", default=0)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Savol-javob"
        verbose_name_plural = "Savol-javoblar"

    def __str__(self):
        return self.question


class ProductPriceMixin:
    """Product klassiga narx va quvvat xususiyatlarini qo'shadi."""

    def _trim_values(self, field):
        return [getattr(t, field) for t in self.trims.all() if getattr(t, field)]

    @property
    def price_from(self):
        v = self._trim_values("price")
        return min(v) if v else None

    @property
    def price_to(self):
        v = self._trim_values("price")
        return max(v) if v else None

    @property
    def power_max(self):
        v = self._trim_values("power_hp")
        return max(v) if v else None

    @property
    def priced_trims_count(self):
        return len(self._trim_values("price"))
