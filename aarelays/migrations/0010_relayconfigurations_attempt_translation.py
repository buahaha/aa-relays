# Generated by Django 3.1.2 on 2020-10-22 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aarelays', '0009_auto_20201022_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='relayconfigurations',
            name='attempt_translation',
            field=models.BooleanField(default=False),
        ),
    ]