# Generated by Django 4.1.4 on 2022-12-17 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_notification"),
    ]

    operations = [
        migrations.AddField(
            model_name="record",
            name="doctor_id",
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]