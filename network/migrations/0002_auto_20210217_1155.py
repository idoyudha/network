# Generated by Django 3.1.5 on 2021-02-17 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='tweet',
            new_name='tweet_text',
        ),
    ]
