# Generated by Django 5.0.2 on 2024-03-17 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="picture",
            field=models.ImageField(blank=True, upload_to="my_picture"),
        ),
    ]