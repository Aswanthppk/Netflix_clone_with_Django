# Generated by Django 3.1.3 on 2021-09-17 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netflix', '0002_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
