# Generated by Django 3.0.10 on 2020-10-26 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20201025_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='token_google',
        ),
        migrations.AddField(
            model_name='user',
            name='id_google',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
