# Generated by Django 4.2.3 on 2023-07-18 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charts", "0004_alter_chart_indicator"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chart",
            name="indicator",
            field=models.IntegerField(null=True),
        ),
    ]
