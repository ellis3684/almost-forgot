# Generated by Django 4.0.3 on 2022-04-08 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_setting_email_address_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Setting',
        ),
    ]