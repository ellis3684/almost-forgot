# Generated by Django 4.0.3 on 2022-04-04 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_settings_setting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
