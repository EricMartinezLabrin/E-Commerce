# Generated by Django 4.0.6 on 2022-08-06 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0016_region_userdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='phone',
            field=models.CharField(max_length=11),
        ),
    ]
