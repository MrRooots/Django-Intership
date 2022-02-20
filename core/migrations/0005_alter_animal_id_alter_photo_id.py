# Generated by Django 4.0.2 on 2022-02-15 14:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_animal_id_alter_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ff2428aa-3dd0-46c5-abb4-5b5d55e18cc8'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='id',
            field=models.UUIDField(default=uuid.UUID('067b05e7-7e8c-4f1d-9693-2cc710e5d4c3'), primary_key=True, serialize=False, unique=True),
        ),
    ]