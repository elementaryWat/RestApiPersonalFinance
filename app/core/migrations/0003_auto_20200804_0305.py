# Generated by Django 3.0.8 on 2020-08-04 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_account_accounttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttype',
            name='icon_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
