# Generated by Django 4.1 on 2022-09-05 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_rename_outcome_record_diagnosis_record_notes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="record",
            name="tests",
            field=models.JSONField(default={"Lab": {}, "Radiology": {}}),
        ),
    ]
