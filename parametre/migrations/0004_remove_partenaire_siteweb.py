# Generated by Django 3.2.6 on 2023-03-07 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parametre', '0003_ouvrage_discipline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partenaire',
            name='siteweb',
        ),
    ]