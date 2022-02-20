# Generated by Django 4.0.2 on 2022-02-15 13:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_animal_birth_year_alter_animal_id_alter_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='id',
            field=models.UUIDField(default=uuid.UUID('dac25d48-e083-4d47-a457-dba921c53177'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='id',
            field=models.UUIDField(default=uuid.UUID('a1a600be-6e8c-4b50-8e5e-7a455e79452b'), primary_key=True, serialize=False, unique=True),
        ),
    ]