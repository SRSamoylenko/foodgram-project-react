# Generated by Django 3.1 on 2021-10-11 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20211011_1249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='colour',
            new_name='color',
        ),
    ]
