# Generated by Django 4.1 on 2022-09-05 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0013_alter_record_tests"),
    ]

    operations = [
        migrations.AlterField(
            model_name="record",
            name="tests",
            field=models.JSONField(default={"lab": {}, "radiology": {}}),
        ),
    ]
