# Generated by Django 4.1 on 2022-09-03 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_patient_blood"),
    ]

    operations = [
        migrations.AddField(
            model_name="record",
            name="outcome",
            field=models.CharField(default="Not set", max_length=1500),
        ),
    ]
