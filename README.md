# Django-Intership
Simple rest-api implementation using python3.8 and Django (pure Django, without rest framework)

### Currently implemented:
  * HEADERS API-KEY validation for each request using `middleware`. Request headers example: {`api-key`: `TEST_API_KEY`}
  * All required endpoints
  * Photo uploading compressing by 50% and saving as a `.jpeg` file inside `core` subdirectory named according to animal.id value
  * Photo downloading by the url
  * SLI Command: `python manage.py export_animals [--has-photos {True, False}]`
  * Application deployed on heroku: `https://animals-intership-api.herokuapp.com/`

### Deployment
  * Inside app folder in cmd run `docker-compose up`
  * Create heroku application: `heroku create <application_name>`
  * Push the container to heroku: `heroku container:push web -a=<application_name>`
  * Boot the application: `heroku container:release web -a=<application_name>`
  * Then you have to install the heroku postgres plugin and inside the heroku cli type: `python manage.py makemigrations`  then `... migrate` to apply migrations on heroku db

### API Usage examples
  * Inside `vendor/` you can find the `my_requests.py` file that contains some request templates to interact with api
