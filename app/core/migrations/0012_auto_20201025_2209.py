# Generated by Django 3.0.10 on 2020-10-25 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_user_token_google'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token_google',
            field=models.CharField(blank=True, max_length=1500),
        ),
    ]