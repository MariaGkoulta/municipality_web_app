# Generated by Django 3.1.1 on 2020-10-01 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipality_project', '0002_auto_20201001_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='deadline',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='activity',
            name='release_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(),
        ),
    ]