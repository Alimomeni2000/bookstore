# Generated by Django 3.2 on 2021-06-20 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_book_discount_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'سفارشات ثبت شده', 'verbose_name_plural': 'سفارشات ثبت شده'},
        ),
        migrations.AlterModelOptions(
            name='orderbook',
            options={'verbose_name': 'سفارش', 'verbose_name_plural': 'سفارشات'},
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('B', 'صورت حساب'), ('S', 'خریدکردن')], default=1, max_length=250, verbose_name='شهر'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(choices=[('B', 'صورت حساب'), ('S', 'خریدکردن')], default=1, max_length=250, verbose_name='استان'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(related_name='books', to='core.Category', verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.SlugField(verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.category', verbose_name='زیر دسته'),
        ),
    ]
