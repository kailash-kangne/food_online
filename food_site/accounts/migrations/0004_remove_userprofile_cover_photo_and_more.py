# Generated by Django 4.1.3 on 2022-11-20 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_userprofile"),
    ]

    operations = [
        migrations.RemoveField(model_name="userprofile", name="cover_photo",),
        migrations.RemoveField(model_name="userprofile", name="profile_picture",),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.PositiveSmallIntegerField(
                blank=True, choices=[(1, "Restaurant"), (2, "Customer")], null=True
            ),
        ),
    ]
