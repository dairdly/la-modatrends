# Generated by Django 3.1 on 2021-01-17 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_product_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='default.jpg', height_field='400', upload_to='images/', width_field='300'),
        ),
    ]
