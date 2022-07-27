# Generated by Django 4.0.6 on 2022-07-27 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0002_remove_banner_extension_banner_datetimeofupload_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('banner', models.FileField(upload_to='categories/')),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='banner',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
