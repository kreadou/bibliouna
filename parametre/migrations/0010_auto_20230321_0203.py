# Generated by Django 3.2.6 on 2023-03-21 02:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('parametre', '0009_alter_article_discipline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='date_soutenance',
        ),
        migrations.AddField(
            model_name='article',
            name='date_parution',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='date parution'),
        ),
    ]
