# Generated by Django 4.1.3 on 2022-12-07 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0016_alter_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.PositiveSmallIntegerField(
                blank=True, choices=[(2, "Customer"), (1, "Vendor")], null=True
            ),
        ),
    ]
