from django.db.models.fields import IntegerField
from django.db.models.signals import post_save
from django.conf import settings
from django_countries.fields import CountryField
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.contrib.contenttypes.fields import GenericRelation

from comment.models import Comment

class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آی پی")

    def __str__(self):
        return self.ip_address

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


ADDRESS_CHOICES = (
    ('B', 'صورت حساب'),
    ('S', 'خریدکردن'),
)


class Category(models.Model):
    parent = models.ForeignKey(
        'self', default=None, null=True, blank=True, on_delete=models.CASCADE,related_name="children")
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=200, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='وضعیت')
    image = models.ImageField(blank=True, null=True,
                              upload_to='category', verbose_name='تصویر')
    icone = models.ImageField(
        blank=True, null=True, upload_to='category', verbose_name='آیکون')

    objects = CategoryManager()

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی ها"
        ordering = ['parent__id']

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل کاربران"

    def __str__(self):
        return self.user.username


class Book(models.Model):

    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ManyToManyField(Category, related_name="books")
    status = models.BooleanField(default=True)
    slug = models.SlugField()
    description = models.TextField()
    pages = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=False)
    author = models.CharField(max_length=200, blank=True, null=False)
    translator = models.CharField(max_length=100, blank=True, null=True)
    publishers = models.CharField(max_length=100, blank=True, null=False)
    special_offer = models.BooleanField(default=False)
    comments = GenericRelation(Comment)
    image = models.ImageField(blank=True, null=True, upload_to='book')
    imageslide = models.ImageField(
        blank=True, null=True, upload_to='book')
    hits= models.ManyToManyField(IPAddress,blank=True,related_name='hits',verbose_name='بازدیدها')
    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'pk': self.pk
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class SlidShow(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدر"
        ordering = ['-book__price']

    def __str__(self):
        return self.book.title


class OrderBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = "سفارش کتاب"
        verbose_name_plural = "سفارشات کتاب"

    def __str__(self):
        return f"{self.quantity} of {self.book.title}"

    def get_total_book_price(self):
        return self.quantity * self.book.price

    def get_total_discount_book_price(self):
        return self.quantity * self.book.discount_price

    def get_amount_saved(self):
        return self.get_total_book_price() - self.get_total_discount_book_price()

    def get_final_price(self):
        if self.book.discount_price:
            return self.get_total_discount_book_price()
        return self.get_total_book_price()


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=250, choices=ADDRESS_CHOICES)
    apartment_address = models.CharField(max_length=250)
    country = CountryField(verbose_name="کشور")
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)

    zip_code = models.CharField(max_length=20, blank=True, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    strip_charge_id = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت ها"


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.FloatField()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "کوپن"
        verbose_name_plural = "کوپن ها"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    books = models.ManyToManyField(OrderBook)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address, blank=True, null=True, related_name='shipping_addresses', on_delete=models.SET_NULL)
    billing_address = models.ForeignKey(
        Address, blank=True, null=True, related_name='billing_addresses', on_delete=models.SET_NULL)
    payment = models.ForeignKey(
        Payment, blank=True, null=True, on_delete=models.SET_NULL)
    coupon = models.ForeignKey(
        Coupon, blank=True, null=True, on_delete=models.SET_NULL)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def get_total(self):
        total = 0
        for order_Book in self.books.all():
            total += order_Book.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class message(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    username = models.CharField(max_length=30)
    password1 = models.CharField(max_length=40)
    password2 = models.CharField(max_length=40)

    contact = models.IntegerField(max_length=15)
    message = models.CharField(max_length=1000, blank=True, null=True)


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    class Meta:
        verbose_name = "مرجوعی"
        verbose_name_plural = "مرجوعی ها"

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
