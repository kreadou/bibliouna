# Generated by Django 3.2.6 on 2023-03-09 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('galerie', '0002_alter_photo_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user',
        ),
    ]
