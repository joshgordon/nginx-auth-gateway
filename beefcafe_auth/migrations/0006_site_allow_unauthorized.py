# Generated by Django 3.0.5 on 2020-04-10 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beefcafe_auth', '0005_auto_20171007_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='allow_unauthorized',
            field=models.BooleanField(default=False),
        ),
    ]