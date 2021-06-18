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
        'self', default=None, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=200, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='وضعیت')
    image = models.ImageField(blank=True, null=True,
                              upload_to='category', verbose_name='تصویر')
    icon = models.ImageField(
        blank=True, null=True, upload_to='category', verbose_name='آیکون')

    objects = CategoryManager()

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی ها"

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="نوار شناسه مشتری")
    one_click_purchasing = models.BooleanField(default=False, verbose_name="خرید با یک کلیک")

    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل کاربران"

    def __str__(self):
        return self.user.username


class Book(models.Model):
    title = models.CharField(max_length=10, verbose_name="عنوان کتاب")
    price = models.FloatField(verbose_name="قیمت کتاب")
    discount_price = models.FloatField(blank=True, null=True, verbose_name="قیمت نهایی")
    category = models.ManyToManyField(Category, verbose_name="دسته بندی")
    status = models.BooleanField(default=True, verbose_name="وضعیت")
    slug = models.SlugField(verbose_name="")
    description = models.TextField(verbose_name="توضیحات")
    pages = models.IntegerField(blank=True, null=True, verbose_name="تعداد صفحات")
    year = models.IntegerField(blank=True, null=False, verbose_name="سال انتشار")
    author = models.CharField(max_length=200, blank=True, null=False, verbose_name="نویسنده")
    translator = models.CharField(max_length=100, blank=True, null=True, verbose_name="مترجم")
    publishers = models.CharField(max_length=100, blank=True, null=False, verbose_name="ناشر")
    special_offer = models.BooleanField(default=False, verbose_name="پیشنهاد ویژه")
    comments = GenericRelation(Comment, verbose_name="نظرات")
    image = models.ImageField(blank=True, null=True, upload_to='book', verbose_name="تصویر")
    imageslide = models.ImageField(
        blank=True, null=True, upload_to='book', verbose_name="اسلاید تصویر")
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
    book = models.OneToOneField(Book, on_delete=models.CASCADE, verbose_name="نام کتاب")
    status = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدر"
        ordering = ['-book__price']

    def __str__(self):
        return self.book.title


class OrderBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False, verbose_name="وضعیت سفارش")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="نام کتاب")
    quantity = models.IntegerField(default=1, verbose_name="تعداد")

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
    street_address = models.CharField(max_length=250, choices=ADDRESS_CHOICES, verbose_name="آدرس خیابان")
    apartment_address = models.CharField(max_length=250, verbose_name="آدرس آپارتمان")
    country = CountryField(verbose_name="کشور")
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES, verbose_name="")
    zip_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="کد پستی")
    default = models.BooleanField(default=False, verbose_name="پیشفرض")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    strip_charge_id = models.CharField(max_length=50, verbose_name="شناسه نوار هزینه")
    amount = models.FloatField(verbose_name="جمع کل خرید")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="زمان")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت ها"


class Coupon(models.Model):
    code = models.CharField(max_length=20, verbose_name="کد کوپن")
    amount = models.FloatField(verbose_name="مقدار")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "کوپن"
        verbose_name_plural = "کوپن ها"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="کد مرجوعی")
    books = models.ManyToManyField(OrderBook, verbose_name="کتاب ها")
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="زمان شروع")
    ordered_date = models.DateTimeField(verbose_name="زمان ثبت سفارش")
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address, blank=True, null=True, related_name='shipping_addresses', on_delete=models.SET_NULL,
        verbose_name="آدرس محل ارسال")
    billing_address = models.ForeignKey(
        Address, blank=True, null=True, related_name='billing_addresses', on_delete=models.SET_NULL,
        verbose_name="آدرس صدور صورتحساب")
    payment = models.ForeignKey(
        Payment, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="پرداخت")
    coupon = models.ForeignKey(
        Coupon, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="کوپن")
    being_delivered = models.BooleanField(default=False, verbose_name="وضعیت سفارش")
    received = models.BooleanField(default=False, verbose_name="وضعیت تحویل")
    refund_requested = models.BooleanField(default=False, verbose_name="درخواست مرجوعی")
    refund_granted = models.BooleanField(default=False, verbose_name="اعطا مرجوعی")

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
    name = models.CharField(max_length=30, verbose_name="نام")
    email = models.EmailField(max_length=40, verbose_name="ایمیل")
    username = models.CharField(max_length=30, verbose_name="نام کاربری")
    password1 = models.CharField(max_length=40, verbose_name="رمز عبور")
    password2 = models.CharField(max_length=40, verbose_name="تکرار رمز عبور")

    contact = models.IntegerField(max_length=15, verbose_name="تماس")
    message = models.CharField(max_length=1000, blank=True, null=True, verbose_name="پیام")


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="سفارش")
    reason = models.TextField(verbose_name="دلیل")
    accepted = models.BooleanField(default=False, verbose_name="")
    email = models.EmailField(verbose_name="ایمیل")

    class Meta:
        verbose_name = "مرجوعی"
        verbose_name_plural = "مرجوعی ها"

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
