# Generated by Django 3.1.5 on 2021-02-27 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_auto_20210221_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]