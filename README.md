ROOMLIST
===

Project Description

On Contributing
---

RoomList welcomes all the help it can get. Even if you don't feel like you can be helpful the more technical aspects, we definitely need designers, technical writers, and testers.

There are many things that can be done with this project (see the "To Do" section), but sometimes it's the small things that count, so don't be afraid of contributing just a small spelling mistake.

If you need help at all please contact a SRCT member. We want people to contribute, so if you are struggling, or just want to learn we are more than willing to help.

The project lead for this project is [Jason Yeomans](jyeoman2@gmu.edu).

Please visit the [SRCT Wiki](http://wiki.srct.gmu.edu/) for more information on this and other SRCT projects, along with other helpful links and tutorials.

Setup
---

To get started, you'll need the following installed:
* [Git](http://git-scm.com/book/en/Getting-Started-Installing-Git)
* Python
* Django 1.7
* PostgreSQL
* Psycopg2
* Other language or framework-specific items

Open a terminal window and type in the following commands. (If you're on Windows, use [Cygwin](http://www.cygwin.com/). This will create a local, workable copy of the project.

``bash``
``git clone git@git.gmu.edu:srct/roomlist.git``
``cd roomlist/``
``A Django project, for example, would include setting up virtual environment, installing from requirements file, setting up south, syncing the database, and runserver``

To set up the PostgreSQL database, open a terminal and type in the following commands:

First, we must install some dependencies for PostgreSQL.

``$ sudo apt-get install libpq-dev python-dev``

Next, we need to install PostgreSQL.

``$ sudo apt-get install postgresql postgresql-contrib``

Now, we need to become the postgres user, create our database, and create our user.

``$ sudo su - postgres``
``$ createdb roomlist``

Choose your username, and execute the next command without the quotes.

``$ createuser -P "your_username"``

You'll then be prompted to twice enter your password. Choose a strong passphrase for production. For local development, password strength is less important.

Finally, we need to enter the PostgreSQL command line interface to grant permissions.

``$ psql``
``postgres=# GRANT ALL PRIVILEGES ON DATABASE roomlist TO django;``

Your PostgreSQL database should now be set up to work with the Roomlist project.

Copy the secret.py.template and config.py.template to secret.py and config.py respectively. For each, follow the comment instruction provided in each file.

Run `python manage.py syncdb` to set up the empty database tables. When you're prompted, say 'y' to setting up the superuser, but use your mason username and full mason email address (@masonlive.gmu.edu) for the account. This is because we use Mason's Central Authentication for our user signin, and your admin account needs to manage your CAS account.

Have your virtualenvironment running and with the requirements.txt installed.

Next, run `python manage.py makemigrations`, `python manage.py migrate`, then `python manage.py runserver`.

Head over to localhost:8000 and see the site!

To-do
---

The list of to-do items is kept track of on the gitlab roomlist issues page. https://git.gmu.edu/srct/roomlist

About GMU SRCT
---

**S**tudent - **R**un **C**omputing and **T**echnology (*SRCT*, pronounced "circuit") is a student organization at George Mason University which enhances student computing at Mason. SRCT establishes and maintains systems which provide specific services for Mason's community.
