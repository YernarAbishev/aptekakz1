from django.contrib.auth.models import User
from django.db import models
from pytils.translit import slugify
from django.urls import reverse
import uuid


class Category(models.Model):
    name = models.CharField("Категория атауы", max_length=255)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категориялар"


class Product(models.Model):
    name = models.CharField(max_length=45)
    price = models.FloatField(default=10.0)
    image = models.ImageField()
    file = models.FileField()
    featured = models.BooleanField(default=False)
    top_product = models.BooleanField(default=False)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, blank=True)
    discount = models.FloatField(default=0.0)
    discounted_price = models.FloatField(default=0.0)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse('product', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.discount > 0:
            self.discounted_price = self.price - self.price * (self.discount/100)
        else:
            self.discounted_price = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

class OrderItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.item)

class Order(models.Model):
    ref_code = models.UUIDField(default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    price = models.FloatField(default=0.0)
    is_processed = models.BooleanField(default=False)


    def __str__(self):
        return str(self.ref_code)


class WishList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.owner)