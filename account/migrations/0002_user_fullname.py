# Generated by Django 2.2.6 on 2019-10-24 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fullname',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
