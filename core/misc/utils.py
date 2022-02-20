import io
import os
import uuid

from pathlib import Path

from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from ..models import Animal, Photo


class Utils:
  """
  Class contains several utility methods:
    - Parse query params
    - Convert string to uuid
    - Save and compress files from POST request
  """

  @staticmethod
  def request_query_params(request: dict) -> list:
    """Parse `limit`, `offset` and `has_photos` params from GET request"""

    try:
      has_photos = request.get('has_photos', None)
      
      if has_photos is not None:
        has_photos = True if has_photos.lower() == 'true' else False
      
      limit, offset = int(request.get('limit', 20)), int(request.get('offset', 0))
    except TypeError:
      limit, offset = 0, 0

    return limit, offset, has_photos

  @staticmethod
  def string_to_uuid(id: str) -> uuid.UUID:
    """Trying to convert string object into uuid. The `uuid.UUID` or `None` will be returned"""
    
    try:
      return uuid.UUID(id)
    except (TypeError, ValueError):
      return None

  @staticmethod
  def compress_image(file: InMemoryUploadedFile) -> io.BytesIO:
    """Compress `InMemoryUploadedFile` and return compressed object as `io.BytesIO`"""
    
    buffer = io.BytesIO()
    Image.open(file.file).save(buffer, 'jpeg', quality=50)
    buffer.seek(0)
    
    return buffer

  @staticmethod
  def save_file(files, animal: Animal) -> dict:
    """
    Save all files from `files: MultiValueDict` to local assets/<animal_id:str>/<filename:str>
    During save operation:
      - Each file will be compressed and converted into <filename:str>.jpeg
      - `Photo` model will be created and saved into database
      ? IDK that to do with files with the same names for one animal, so I chose to simply overwrite the file...
      ? Other possible solutions: create new model object + file_<i>.extension | return exception
    """

    saved_photos = []
    try:
      file_directory = os.path.join(settings.MEDIA_ROOT, str(animal.id))
      
      # parents=True -> create all intermediate folders
      # exist_ok=True -> skip operation if folder already exists
      Path(file_directory).mkdir(parents=True, exist_ok=True)
      
      for _field_name in files.keys():
        for file_object in files.getlist(_field_name):
          filename = file_object.name.split(".")[0] + '.jpeg'
          path = os.path.join(file_directory, filename)
          
          print('[Utils.save_file]: Saving {} into {}'.format(file_object, path))
          
          if not Path(path).is_file():
            saved_photos.append(Photo.objects.create(filename=filename))
          else:
            saved_photos.append(animal.photos.get(filename__iexact=filename))
          
          with open(path, 'wb') as local_file:
            local_file.write(Utils.compress_image(file_object).read())

      return {
        'success': True,
        'photos': saved_photos,
      }
    except (TypeError, FileNotFoundError, ValueError, IndexError) as error:
      return {
        'success': False, 
        'error': error
      }
