import json
import os
from django.conf import settings

from django.http import HttpResponse, JsonResponse
from django.views import View

from vendor.responses import ResponseCodes, Responses
from .misc.utils import Utils

from .models import Animal


class AnimalsView(View):
  """
    View handles requests to /pets url:
      - GET:    get animals data as `JsonResponse`
      - POST:   create animal record in database
      - DELETE: delete aniamal record and all dependent records
  """

  def get(self, request) -> JsonResponse:
    limit, offset, has_photos = Utils.request_query_params(request=request.GET)

    if has_photos is None:
      animals = Animal.objects.all()[offset:offset+limit]
    else:
      animals = Animal.objects.filter(photos__isnull=not has_photos)[offset:offset+limit]

    return JsonResponse(
      data={
        'count': animals.count(),
        'items': [animal.to_json(request) for animal in animals]
      },
      status=ResponseCodes.OK,
    )
  
  def post(self, request) -> JsonResponse:
    body = request.body.decode()

    try:
      animal_json = dict(json.loads(body))
    
      created_animal = Animal.objects.create(
        name=animal_json['name'], 
        type=animal_json['type'],
        birth_year=animal_json['birth_year'],
      )

      return JsonResponse(data=created_animal.to_json(request), status=ResponseCodes.CREATED)
    except (json.JSONDecodeError, TypeError) as error:
      return Responses.bad_request(f'[POST /pets]: Invalid data format recieved: {body}.')
    except KeyError as key:
      return Responses.bad_request(f'[POST /pets]: Required fields {key} not provided: {body}.')

  def delete(self, request) -> JsonResponse:
    try:
      body = request.body.decode()
      response = {
        "deleted": 0,
        "errors": []
      }
      status_code = ResponseCodes.OK
      ids = dict(json.loads(body)).get('ids', [])
      
      for id in ids:
        uuid = Utils.string_to_uuid(id)
        
        if uuid is None:
          response['errors'].append(
            {
              'id': id,
              'error': 'Invalid id format.'
            }
          )
        else:
          try:
            Animal.objects.get(id__exact=uuid).delete()
            response['deleted'] += 1
          except Animal.DoesNotExist:
            response['errors'].append(
              {
                'id': uuid,
                'error': 'Pet with the matching ID was not found.'
              }
            )

      return JsonResponse(data=response, status=status_code)
    
    except (json.JSONDecodeError, TypeError) as error:
      return Responses.bad_request(f'[POST /pets]: Invalid data format recieved: {body}')


class AnimalPhotoView(View):
  """
    View handles 
      - upload photo POST request to selected animal
      - download photo GET request
  """

  def post(self, request, animal_id: str) -> JsonResponse:
    animal_uuid = Utils.string_to_uuid(animal_id)
    
    if animal_uuid:
      try:
        animal = Animal.objects.get(id__exact=animal_uuid)

        # Trying to load and save the received files to core/assets/<animal_id>/ folder
        save_result = Utils.save_file(files=request.FILES, animal=animal)
        
        if save_result['success']:
          photo_count = 0
          for saved_photo in save_result['photos']:
            animal.photos.add(saved_photo)
            photo_count += 1
          
          if photo_count > 1:
            data=[
              {
                'id': photo.id,
                'url': photo.get_absolute_url(request),
              } for photo in save_result['photos']
            ]
          else:
            data={
              'id': save_result['photos'][0].id,
              'url': save_result['photos'][0].get_absolute_url(request),
            }
          return JsonResponse(data=data, status=ResponseCodes.OK)
        else:
          return Responses.internal_server_error(animal_id, str(save_result['error']))
      except Animal.DoesNotExist:
        return Responses.animal_not_exist(animal_id)
    else:
      return Responses.invalid_id(animal_id)

  def get(self, _, animal_id: str, filename: str):
    try:
      Animal.objects.get(id__exact=animal_id)
      
      with open(os.path.join(settings.MEDIA_ROOT, animal_id, filename), 'rb') as file:
        return HttpResponse(file.read(), content_type='image/png')
    except Animal.DoesNotExist:
      return Responses.animal_not_exist(animal_id)

