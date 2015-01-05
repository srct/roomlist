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

``First, we must install some dependencies for PostgreSQL.``
``$ sudo apt-get install libpq-dev python-dev``
``Next, we need to install PostgreSQL.``
``$ sudo apt-get install postgresql postgresql-contrib``
``Now, we need to become the postgres user, create our database, and create our user.``
``$ sudo su - postgres``
``$ createdb roomlist``
``$ createuser -P``
``Now follow the prompts, the username should be "django" (without the qoutes) and the password should be "H0jrp0llTJ" (without the qoutes). Next enter 'n' and press "Enter" for the following three promts.``
``Finally, we need to enter the PostgreSQL command line interface to grant permissions.``
``$ psql``
``postgres=# GRANT ALL PRIVILEGES ON DATABASE roomlist TO django;``
Your PostgreSQL database should now be set up to work with the Roomlist project.


Next, run `python manage.py migrate`, then `python manage.py runserver`.
Have your virtualenvironment running and with the requirements.txt installed.

To-do
---

Note-- this should also be on the wiki

About GMU SRCT
---

**S**tudent - **R**un **C**omputing and **T**echnology (*SRCT*, pronounced "circuit") is a student organization at George Mason University which enhances student computing at Mason. SRCT establishes and maintains systems which provide specific services for Mason's community.
