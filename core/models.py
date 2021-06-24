from django.db.models.fields import IntegerField
from django.db.models.signals import post_save
from django.conf import settings
from django_countries.fields import CountryField
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.contrib.contenttypes.fields import GenericRelation
from extensions.utils import jalali_converter
from comment.models import Comment
# Create your models here.
from django.utils.html import format_html

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


BEING_DELIVERED = (
    ('S', 'در صف بررسی'),
    ('C', 'تایید سفارش'),
    ('P', 'آماده سازی سفارش'),
    ('p', 'بسته بندی'),
    ('D', 'تحویل به پست'),
    ('c', 'تحویل مشتری'),
)

class Category(models.Model):
    parent = models.ForeignKey(
        'self', default=None, null=True, blank=True, on_delete=models.SET_NULL,related_name="children",verbose_name="زیر دسته")
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=200, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='وضعیت')
    image = models.ImageField(blank=True, null=True,
                              upload_to='category', verbose_name='تصویر')
    icon = models.ImageField(
        blank=True, null=True, upload_to='category', verbose_name='آیکون')

    objects = CategoryManager()
    def get_absolute_url(self):
        return reverse("account:category-list")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی ها"
        ordering =['parent__id']
        

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="شناسه مشتری")
    one_click_purchasing = models.BooleanField(default=False, verbose_name="خرید")
    def get_absolute_url(self):
        return reverse("account:user-list")
    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل کاربران"

    def __str__(self):
        return self.user.username


class Book(models.Model):
    title = models.CharField(max_length=10, verbose_name="عنوان کتاب")
    price = models.FloatField(verbose_name="قیمت کتاب")
    discount_percent = models.FloatField(default=0,blank=True, null=True, verbose_name="درصد تخفیف")
    category = models.ManyToManyField(Category,related_name="books", verbose_name="دسته بندی")
    status = models.BooleanField(default=True, verbose_name="وضعیت")
    slug = models.SlugField(verbose_name="آدرس")
    description = models.TextField(verbose_name="توضیحات")
    pages = models.IntegerField(blank=True, null=True, verbose_name="تعداد صفحات")
    year = models.IntegerField(blank=True, null=False, verbose_name="سال انتشار")
    author = models.CharField(max_length=200, verbose_name="نویسنده")
    translator = models.CharField(max_length=100, verbose_name="مترجم")
    publishers = models.CharField(max_length=100, verbose_name="ناشر")
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
    def category_to_str(self):
        return "، ".join([category.title for category in self.category.active()])
    category_to_str.short_description = "دسته‌بندی"

    def value_discount(self):
        if self.discount_percent != 0:
            num= self.discount_percent
            return num

    value_discount.short_description = "درصد تخفیف"
    
    def discount_price(self):
        if self.value_discount == 0:
            return int(self.price)
        else:
            return int(self.price-(self.price*self.discount_percent/100))
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
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def __str__(self):
        return f"{self.quantity} of {self.book.title}"

    def get_total_book_price(self):
        return self.quantity * self.book.price

    def get_total_discount_book_price(self):
        return self.quantity * self.book.discount_price()

    def get_amount_saved(self):
        return self.get_total_book_price() - self.get_total_discount_book_price()

    def get_final_price(self):
        if self.book.discount_price():
            return self.get_total_discount_book_price()
        return self.get_total_book_price()


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=250, verbose_name="آدرس خیابان")
    city = models.CharField(max_length=250, verbose_name="شهر")
    state = models.CharField(max_length=250 ,verbose_name="استان")

    apartment_address = models.CharField(max_length=250, verbose_name="آدرس آپارتمان")
    country = CountryField(verbose_name="کشور")
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES, verbose_name="انتخاب آدرس")
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
    strip_charge_id = models.CharField(max_length=50, verbose_name="شناسه پرداخت")
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
    def get_absolute_url(self):
        return reverse("account:coupon-list")
    # def get_absolute_url(self):
    #     return reverse("account:coupon-delete", kwargs={
    #         'pk': self.pk
    #     })
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
    being_delivered = models.CharField(max_length=1,choices=BEING_DELIVERED,default='S', verbose_name="وضعیت سفارش")
    received = models.BooleanField(default=False, verbose_name="وضعیت تحویل")
    refund_requested = models.BooleanField(default=False, verbose_name="درخواست مرجوعی")
    refund_granted = models.BooleanField(default=False, verbose_name="اعطا مرجوعی")
    def jorderd_date(self):
        return jalali_converter(self.ordered_date)
    jorderd_date.short_description = "زمان ثبت سفارش"
    def get_absolute_url(self):
        return reverse("account:order-list")
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "سفارشات ثبت شده"
        verbose_name_plural = "سفارشات ثبت شده"

    def get_total(self):
        total = 0
        for order_Book in self.books.all():
            total += order_Book.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def books_to_list(self):
        return (books.book for books in self.books.all())
    books_to_list.short_description = "لیست کتاب ها"
    # def get_absolute_url(self):
    #     return reverse("account:order-list")
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
    reason = models.TextField(verbose_name="توضیحات")
    accepted = models.BooleanField(default=False, verbose_name="وضعیت")
    email = models.EmailField(verbose_name="ایمیل")
    def get_absolute_url(self):
        return reverse("account:refund-list")
    class Meta:
        verbose_name = "مرجوعی"
        verbose_name_plural = "مرجوعی ها"

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
