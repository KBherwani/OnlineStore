# Generated by Django 4.0.5 on 2022-06-28 06:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("product", "0002_products"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Products",
            new_name="Product",
        ),
    ]
