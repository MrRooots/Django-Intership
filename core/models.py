import os
import uuid
import shutil
import datetime

from django.db import models, IntegrityError
from django.conf import settings
from django.urls import reverse

from .misc.serializer import AnimalToJsonSerializer


class Animal(models.Model):
  """
  Animal model description
  """

  # Animal id in database
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4())
  
  # Animal type { Dog | Cat }
  type = models.CharField(max_length=3, db_index=True)
  
  # Animal name
  name = models.CharField(max_length=128, db_index=True)
  
  # Animal birth year { Positive integer: 0 to 32767 }
  birth_year = models.PositiveSmallIntegerField(null=False)

  # Animal record creation date
  created_at = models.DateTimeField(auto_now_add=True)

  @property
  def age(self) -> int:
    """Animal age will be computed from `created_at` and current date"""
    return datetime.datetime.now().year - self.birth_year

  
  def to_json(self, request=None, include_photo_id=True) -> dict:
    """Get full information about the animal as a json"""
    return AnimalToJsonSerializer.to_json(self, request, include_photo_id)

  def save(self, *args, **kwargs) -> None:
    """Override the `save` method to set the id of type `UUID` of the animal"""
    try:
      super(Animal, self).save(*args, **kwargs)
    except IntegrityError:
      self.id = uuid.uuid4()
      super(Animal, self).save(*args, **kwargs)

  def delete(self, using=None, keep_parents=False) -> None:
    """Override the `delete` method to delete all dependent files while db record delete"""
    for photo in self.photos.all():
      photo.delete()

    try:
      shutil.rmtree(os.path.join(settings.MEDIA_ROOT, str(self.id)))
    except (FileNotFoundError, PermissionError) as error:
      print(f'Error during direction delete! {error}')
      print(f'Trying to delete this path: {os.path.join(settings.MEDIA_ROOT, str(self.id))}')

    super(Animal, self).delete()

  def __str__(self) -> str:
    return f'{self.name} is a {self.type} of {self.age} years old'


class Photo(models.Model):
  """
  Photo model description
  """

  # Photo id
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4())
  
  # Photo file name
  filename = models.CharField(max_length=255)
  
  # Animal dependency
  animal = models.ForeignKey(
    'Animal', 
    on_delete=models.CASCADE, 
    related_name='photos', 
    null=True, 
    blank=True,
  )

  # ? IDK better method to get the absolute file uri without reference to `request` object
  # ? and without using FileField.url
  # ? So the absolute file url is built from setting.ALLOWED_HOSTS when requested from CLI
  def get_absolute_url(self, request) -> str:
    """Build an absolute url for the photo file and return it as a string"""
    
    params = reverse(
      'get_photo',
      kwargs={
        "animal_id": self.animal.id, 
        "filename": self.filename,
      },
    )
    return request.build_absolute_uri(params) if request else settings.ALLOWED_HOSTS[0][:-1] + params

  def save(self, *args, **kwargs) -> None:
    """Override the save method to set the id of type UUID for the photo"""
    
    try:
      super(Photo, self).save(*args, **kwargs)
    except IntegrityError:
      self.id = uuid.uuid4()
      super(Photo, self).save(*args, **kwargs)
