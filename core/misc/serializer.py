# Provide serialization methods for [Animal] model
class AnimalToJsonSerializer:
  @staticmethod
  def to_json(model, request, include_photo_id) -> dict:
    return {
      "id": str(model.id),
      "name": model.name,
      "age": model.age,
      "type": model.type,
      "photos": [
        {
          "id": str(photo.id), 
          "url": photo.get_absolute_url(request)
        } for photo in model.photos.all()
      ] if include_photo_id else [
        photo.get_absolute_url(request) for photo in model.photos.all()
      ],
      "created_at": model.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
    }
