# Generated by Django 3.1.3 on 2021-09-18 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netflix', '0006_auto_20210918_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='trailer_url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]