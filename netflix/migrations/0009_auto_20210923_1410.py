# Generated by Django 3.1.3 on 2021-09-23 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netflix', '0008_list_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='description',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='list',
            name='short_description',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]