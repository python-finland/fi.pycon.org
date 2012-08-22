Introduction
------------

This is the source code for PyCon Finland website:
http://fi.pycon.org/.

All source code is licensed under `BSD license
<http://www.opensource.org/licenses/bsd-license.php>`_.

Running the site
-------------------

Commands to start the site locally::

    git@github.com:python-finland/fi.pycon.org.git

* Requirements:
    - Virtualenv
    - Django (1.3+)
    - South

* How to:
    - Frontend of the site is located in /<year> folder (like 2011 or 2012), they are just pure HTML files
    - Backend of the site is located in /api/pycon<year> folder. To run backend, go to /api folder and run: python manage.py runserver

The production server
-----------------------

In your ``.ssh/config`` add::

    # fi.pycon.org django server
    Host pythonfi
    ForwardAgent yes
    User pythonfi
    Hostname vps1207.zoner-asiakas.fi

Now you can type::

    ssh pythonfi

Restart the production server::

    screen -x # screen if not active yet
    cd /srv/fi.pycon.org/
    source ../virtualenv/bin/activate
    killall python; sleep 1; virtualenv/bin/python www/api/manage.py runfcgi host=127.0.0.1 port=8080

Repos
-----

The official source code repository is
https://github.com/python-finland/fi.pycon.org/.

Contact
-------

Regarding any questions please contact the `board members
<hallitus@python.fi>`_ of the Python Finland association, or the
`PIG-Fi mailing list <http://groups.google.com/group/pigfi>`_.
