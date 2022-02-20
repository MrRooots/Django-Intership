from django.http import HttpResponse, JsonResponse


class ResponseCodes:
  """
  Class contains server response codes
  """

  OK = 200
  CREATED = 201
  BAD_REQUEST = 400
  UNAUTHORIZED = 401
  METHOD_NOT_ALLOWED = 405
  INTERNAL_SERVER_ERROR = 500


class Responses:
  """
  Class contains templates of server `JsonResponse`. 
  """

  @staticmethod
  def invalid_id(id: str) -> JsonResponse:
    """
    Invalid animal `id` format provided during request
    """
    return JsonResponse(
      data={
        'id': id,
        'error': 'Invalid id format.'
      },
      status=ResponseCodes.BAD_REQUEST,
    )
  
  @staticmethod
  def animal_not_exist(id: str) -> JsonResponse:
    """
    Animal with provided `id` does not exist in database
    """
    return JsonResponse(
        data={
          "errors": [
            {
              "id": id, 
              "error": "Pet with the matching ID was not found."
            }
          ]
        }, 
        status=ResponseCodes.OK,
      )

  @staticmethod
  def internal_server_error(id: str, error: str) -> JsonResponse:
    """
    Internal server `error` during handling request for [photo | animal] with `id`
    """
    return JsonResponse(
      data={
        'errors': [
          {
            'id': id,
            'error': error
          }
        ],
      },
      status=ResponseCodes.INTERNAL_SERVER_ERROR,
    )

  @staticmethod
  def bad_request(errorMessage: str) -> JsonResponse:
    """
    Invalid request. `errorMessage` describes the error
    """
    return JsonResponse(
      data={
        'errors': [
          {
            'error': errorMessage,
          }
        ]
      },
      status=ResponseCodes.BAD_REQUEST,
    )

  