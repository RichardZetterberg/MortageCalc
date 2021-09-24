# eliftechITTest
Web application where users can create, delete or update banks and calculate mortgage payments using one of these bank’s settings.

***

## Extension:
- SQL ORM: https://flask-sqlalchemy.palletsprojects.com/en/2.x/

## Installation:
Install with pip:
```python
$ pip install -r requirements.txt
```

***

## Run Flask

# Run flask for develop
```
$ python main.py
```
In flask, Default port is 5000
Swagger document page: http://127.0.0.1:5000/

# Run flask for production
** Run with gunicorn **
```
$ gunicorn -w 4 -b 127.0.0.1:5000 main:app
```

- -w : number of worker
- -b : Socket to bind

***

## Reference:
Offical Website
- [Flask]https://flask.palletsprojects.com/en/2.0.x/
- https://flask.palletsprojects.com/en/2.0.x/extensions/
- https://flask-sqlalchemy.palletsprojects.com/en/2.x/
- https://gunicorn.org/


Tutorial
- https://www.slideshare.net/maxcnunes1/flask-python-16299282
- https://igordavydenko.com/talks/ua-pycon-2012.pdf

https://github.com/tsungtwu/flask-example/wiki
