# Generated by Django 4.1.4 on 2022-12-13 20:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(name="Doctor",),
        migrations.AddField(
            model_name="patient",
            name="doctor",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="user",
            name="specialization",
            field=models.CharField(
                choices=[
                    ("General Practitioner", "General Practitioner"),
                    ("Internal Medicine", "Internal Medicine"),
                    ("Dermatology", "Dermatology"),
                    ("Pediatrics", "Pediatrics"),
                    ("Gynecology", "Gynecology"),
                    ("Cardiology", "Cardiology"),
                    ("Laboratory", "Laboratory"),
                ],
                max_length=50,
            ),
        ),
    ]