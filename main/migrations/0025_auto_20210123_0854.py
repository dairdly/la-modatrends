# Generated by Django 3.1.5 on 2021-01-23 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20210123_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('IN PROGRESS', 'In Progress'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], default='CREATED', max_length=11),
        ),
    ]