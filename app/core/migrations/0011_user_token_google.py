# Generated by Django 3.0.10 on 2020-10-25 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_transactioncategory_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token_google',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
