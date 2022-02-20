import json
from django.core.management.base import BaseCommand, CommandParser, CommandError
from core.models import Animal, Photo

class Command(BaseCommand):
  """
  Custom export animals CLI command defenition
  """

  help = 'Export all animals from database in json format'

  def add_arguments(self, parser: CommandParser) -> None:
    parser.add_argument(
      '--has-photos',
      choices=['True', 'False'],
      help='Export only animals with or without photo',
    )

  def handle(self, *args, **options) -> str:
    has_photos = options.get('has_photos', None)
    
    if has_photos is None:
      content = [animal.to_json(include_photo_id=False) for animal in Animal.objects.all()]
    else:
      has_photos = True if has_photos.lower() == 'true' else False
      content = [
        animal.to_json(include_photo_id=False) 
        for animal in Animal.objects.filter(photos__isnull=not has_photos)
      ]
    
    self.stdout.write(json.dumps({'pets': content}, indent=2))
  
