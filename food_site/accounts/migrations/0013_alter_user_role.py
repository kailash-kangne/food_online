# Generated by Django 4.1.3 on 2022-12-06 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_alter_user_role"),
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
