Introduction
------------

This is the source code for PyCon Finland website:
http://fi.pycon.org/.

All source code is licensed under `BSD license
<http://www.opensource.org/licenses/bsd-license.php>`_.

Running the site
-------------------

* Requirements:
    - Virtualenv
    - Django (1.3+)
    - South
    - 1 "secret" file located outside the root folder, name it "secret", so for example you have the root folder of the project is /home/yourhome/dev/pycon/, the secret file should be /home/yourhome/dev/secret
    - 1 sqlite3 file located outside the root folder, name it "db2012.sqlite3"

* How to:
    - Frontend of the site is located in /<year> folder (like 2011 or 2012), they are just pure HTML files
    - Backend of the site is located in /api/pycon<year> folder. To run backend, go to /api folder and run: python manage.py runserver

Commands to duplicate the production site locally. First see how to add your SSH key below::

    git@github.com:python-finland/fi.pycon.org.git
    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py venv  # Create virtualenv
    source venv/bin/activate
    pip install Django South
    scp pythonfi:/srv/fi.pycon.org/db2012.sqlite3 .
    cd api
    touch ../../secret # Create secret file
    python manage.py runserver

The production server
-----------------------

In your ``.ssh/config`` add::

    # fi.pycon.org django server
    Host pythonfi
    ForwardAgent yes
    User pythonfi
    Hostname vps1207.zoner-asiakas.fi

Add your SSH key to the server using the organization password::

    ssh-copy-id pythonfi

Now you can enter the server::

    ssh pythonfi

Restart and refresh the production server::

    screen -x # screen if not active yet
    cd /srv/fi.pycon.org/www
    source ../virtualenv/bin/activate
    git pull # Load new code from github
    killall python; sleep 1; virtualenv/bin/python www/api/manage.py runfcgi host=127.0.0.1 port=8080

... or ... ::

    killall python; sleep 1; cd /srv/fi.pycon.org/www ; git pull ; ../virtualenv/bin/python api/manage.py runfcgi host=127.0.0.1 port=8080

Editing the pages
--------------------

Example::

    cd fi.python.org
    python -m SimpleHTTPServer

Then

    http://localhost:8000/2012/demo.html

Repos
-----

The official source code repository is
https://github.com/python-finland/fi.pycon.org/.

Github hooks
---------------

CIA will post commit data to #python-hallitus @ IRCNet.

Get Github hook debug data::

    curl -u "miohtama:xxxx" -in https://api.github.com/repos/python-finland/fi.pycon.org/hooks

Contact
-------

Regarding any questions please contact the `board members
<hallitus@python.fi>`_ of the Python Finland association, or the
`PIG-Fi mailing list <http://groups.google.com/group/pigfi>`_.
