# Generated by Django 3.1 on 2020-08-15 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200815_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('clothing', 'Clothing'), ('crafts', 'Crafts'), ('home', 'Home'), ('pet', 'Pet')], max_length=10),
        ),
    ]