# Generated by Django 3.1.5 on 2021-02-27 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_auto_20210227_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='imageURL',
            field=models.URLField(blank=True, null=True),
        ),
    ]