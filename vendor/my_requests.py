"""Module contains various requests to manipulate and test available server operations"""

import json
import random
import requests
import multiprocessing

class MyRequests:
  """Contains a lot of various requests to manipulate and test available server operations"""
  
  # Main url
  URL = 'http://127.0.0.1:8000/pets/'
  
  # Each request headers
  HEADERS = {'api-key': 'TEST_API_KEY'}
  
  # List of names. Used to generate random animals
  NAMES = [
    'Snaveepseo', 'Alliccea', 'Waluloor', 'Mosqeolsa', 'Qouceon', 'Qokerine', 'Virsealing', 'Getseeboon',
    'Crookleame', 'Slubbok', 'Hippacle', 'Skunadillo',
    'Giragrede', 'Toaplucsa', 'Wolivet', 'Seramoom', 'Xoukserpillar', 'Garsupine', 'Klaukseoroach', 'Briboon', 'Ligrou',
    'Poukaam', 'Waringale', 'Flamigator', 'Weammaak', 'Wealloun', 'Walaagaas', 'Rabopsaum', 'Lauksarak', 'Vaupsopotamus',
    'Dreatstile', 'Caacshog', 'Geoqooc', 'Leessooli', 'Snakossum', 'Crocish', 'Toastroops', 'Moomani', 'Skunaafeesa',
    'Coyaansacee', 'Kleecoth', 'Striraros', 'Beecshog', 'Zeophin', 'Kleatoo', 'Geogsouts', 'Mulander', 'Poroose',
    'Buffanaupsi', 'Locuksoursi', 'Quadeopsaumeo', 'Serousreecs', 'Fumida', 'Crusaroo', 'Ceonraffe', 'Peomumadillo',
    'Ticcau', 'Raalsoops', 'Skunish', 'Wolvingo'
  ]

  # Animal birth dates limits
  START_YEAR, END_YEAR = 1990, 2022

  @property
  def _random_animal(self) -> dict:
    """Generate random animal"""
    return {
      'name': random.choice(self.NAMES),
      'type': random.choice(['cat', 'dog']),
      'birth_year': random.randint(self.START_YEAR, self.END_YEAR)
    }

  def _make_post(self, _=None) -> requests.Response:
    """Make the POST request to create animal"""
    r = requests.post(self.URL, headers=self.HEADERS, json=self._random_animal)
    print(f'[{r}]: {r.text}')
    return r
  
  def spawn_animals(self, count: int=100) -> None:
    """Create `count` animal records in database"""
    with multiprocessing.Pool(processes=multiprocessing.cpu_count() * 2) as pool:
      pool.map(self._make_post, [i for i in range(count)])

  def clear_database(self) -> None:
    """Delete all animals from database"""
    animals = requests.get(
      url=self.URL+'?limit=10000', 
      headers=self.HEADERS
    )

    requests.delete(
      url=self.URL, 
      headers=self.HEADERS, 
      data=json.dumps(
        {
          "ids": [i['id'] for i in animals.json()['items']]
        }
      )
    )

  def spawn_animal_with_photo(self):
    """Create new animal record and upload photo"""
    animal_id = json.loads(self._make_post().content)['id']
    requests.post(
      url=f'{self.URL}{animal_id}/photo/',
      headers=self.HEADERS,
      files={'animal_img': open('test_image.jpg','rb')}
    )

  def execute_operations_check(self) -> None:
    """Execute all methods allowed on server and print responses to console"""
    pass


if __name__ == '__main__':
  my_requests = MyRequests()
  my_requests.clear_database()
  # my_requests.spawn_animals(count=100)
  # my_requests.spawn_animal_with_photo()
