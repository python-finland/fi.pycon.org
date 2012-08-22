Introduction
------------

This is the source code for PyCon Finland website:
http://fi.pycon.org/.

All source code is licensed under `BSD license
<http://www.opensource.org/licenses/bsd-license.php>`_.

Running the site
-------------------


    git@github.com:python-finland/fi.pycon.org.git
    
* Requirements:
    - Virtualenv
    - Django (1.3+)
    - South
    - 1 "secret" file located outside the root folder, name it "secret", so for example you have the root folder of the project is /home/yourhome/dev/pycon/, the secret file should be /home/yourhome/dev/secret
    - 1 sqlite3 file located outside the root folder, name it "db2012.sqlite3"

* How to:
    - Frontend of the site is located in /<year> folder (like 2011 or 2012), they are just pure HTML files
    - Backend of the site is located in /api/pycon<year> folder. To run backend, go to /api folder and run: python manage.py runserver

Repos
-----

The official source code repository is
https://github.com/python-finland/fi.pycon.org/.

Contact
-------

Regarding any questions please contact the `board members
<hallitus@python.fi>`_ of the Python Finland association, or the
`PIG-Fi mailing list <http://groups.google.com/group/pigfi>`_.
