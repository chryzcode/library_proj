# Generated by Django 5.1 on 2024-09-17 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowbook',
            old_name='books',
            new_name='book',
        ),
    ]
