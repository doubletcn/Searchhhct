# Generated by Django 4.1 on 2023-04-16 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_auto_20210322_2234"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="tags",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]