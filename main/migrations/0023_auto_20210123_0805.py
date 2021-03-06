# Generated by Django 3.1.5 on 2021-01-23 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20210123_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='apartment',
            field=models.CharField(blank=True, default='', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(blank=True, default='', max_length=30, null=True),
        ),
    ]
