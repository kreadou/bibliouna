# Generated by Django 3.2.6 on 2022-10-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abonne', '0002_auto_20221028_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonne',
            name='regle',
            field=models.BooleanField(blank=True, default=False, verbose_name='reglé'),
        ),
    ]