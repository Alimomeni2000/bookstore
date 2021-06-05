# Generated by Django 3.2 on 2021-06-05 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210605_1900'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'دسته\u200cبندی', 'verbose_name_plural': 'دسته\u200cبندی ها'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='book',
            name='category',
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.category'),
            preserve_default=False,
        ),
    ]
