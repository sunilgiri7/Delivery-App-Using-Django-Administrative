# Generated by Django 4.2 on 2023-04-08 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_menuitem_options_ordermodel_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
