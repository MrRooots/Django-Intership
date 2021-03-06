# Generated by Django 4.0.2 on 2022-04-22 09:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_animal_id_alter_photo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='id',
            field=models.UUIDField(default=uuid.UUID('8f1a8d9b-ea6a-4a56-99f8-57a09ab49ddc'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='id',
            field=models.UUIDField(default=uuid.UUID('a28a3b83-5987-44c6-8d97-15aebd919994'), primary_key=True, serialize=False, unique=True),
        ),
    ]
