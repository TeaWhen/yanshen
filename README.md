yanshen
=======


Dev Setup
=======

1. `sudo pip install virtualenv`
2. `virtualenv dev15` (in root `yanshen`)
3. `source dev15/bin/activate`
4. `wget https://github.com/django/django/archive/1.5b2.tar.gz`
5. `tar xzf 1.5b2.tar.gz`
6. `cd django-1.5b2`
7. `python setup.py install`
8. `rm -rf django-1.5b2`
9. `pip install -r dj15req.txt`