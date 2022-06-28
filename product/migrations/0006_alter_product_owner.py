# Generated by Django 4.0.5 on 2022-06-28 09:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("product", "0005_rename_categories_categorie"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
