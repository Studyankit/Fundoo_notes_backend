# Generated by Django 4.0.4 on 2022-06-03 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verify',
            field=models.BooleanField(default=False),
        ),
    ]
