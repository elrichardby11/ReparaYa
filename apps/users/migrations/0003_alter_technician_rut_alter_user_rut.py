# Generated by Django 5.1.2 on 2024-10-16 01:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_rename_created_at_user_date_joined_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="technician",
            name="rut",
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="rut",
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]