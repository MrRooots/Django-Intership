# Generated by Django 4.0.2 on 2022-02-14 09:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='birth_year',
            field=models.PositiveSmallIntegerField(default=2006),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='animal',
            name='id',
            field=models.UUIDField(default=uuid.UUID('479ba7e9-e4bc-4b8d-b227-a674bd619b47'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1090788a-ede7-47b7-b218-e1dcf4746b8d'), primary_key=True, serialize=False, unique=True),
        ),
    ]
