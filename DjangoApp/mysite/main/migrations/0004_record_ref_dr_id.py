# Generated by Django 4.1.4 on 2022-12-15 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_rename_doctor_patient_doctors"),
    ]

    operations = [
        migrations.AddField(
            model_name="record", name="ref_dr_id", field=models.IntegerField(null=True),
        ),
    ]