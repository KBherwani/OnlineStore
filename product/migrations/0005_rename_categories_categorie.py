# Generated by Django 4.0.5 on 2022-06-28 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_rename_category_categories"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Categories",
            new_name="Categorie",
        ),
    ]
