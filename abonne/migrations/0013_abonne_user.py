# Generated by Django 3.2.6 on 2023-03-21 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('abonne', '0012_auto_20230321_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='abonne',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name="nom d'utilisateur"),
            preserve_default=False,
        ),
    ]