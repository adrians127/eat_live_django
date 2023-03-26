# eat-live
A web application for counting calories
## Get started
In repository folder write commands:
```
pipenv install django
pip install python-decouple
```
Make your own SECRET_KEY. You can generate it from python interpreter:
```
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```
Then paste this key to .env file and add:
```
DEBUG=True/False
```
