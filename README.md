# Hasker 
Q/A site, analogue of stackoverflow.com

### Requirements
- Python (3.6+)
- Django (2.2+)

### Development environment installation

1. Install requirements
```
pip install -r requirements-dev.txt
```

2. Apply migrations
```
python manage.py makemigrations
python manage.py migrate
```

3. Run tests
```
python manage.py test
```

To run server:
```
python manage.py runserver
```