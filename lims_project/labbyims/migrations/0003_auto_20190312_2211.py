# Generated by Django 2.1.6 on 2019-03-12 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labbyims', '0002_auto_20190312_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
