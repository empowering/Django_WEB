# Generated by Django 3.1 on 2020-08-14 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200814_1139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='bidder',
            new_name='likes',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]