# Generated by Django 3.1.5 on 2021-02-27 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_auto_20210227_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='imageURL',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='network.profile'),
        ),
    ]
