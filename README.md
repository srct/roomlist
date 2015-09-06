# ROOMLIST

Roomlist is a secure, privacy-oriented service for Mason studens to find their on-campus neighbors.

## On Contributing

RoomList welcomes all the help it can get. Even if you don't feel like you can be helpful the more technical aspects, we definitely need designers, technical writers, and testers.

There are many things that can be done with this project (see the "To Do" section), but sometimes it's the small things that count, so don't be afraid of contributing just a small spelling mistake.

If you need help at all please contact a SRCT member. We want people to contribute, so if you are struggling, or just want to learn we are more than willing to help.

The project manager for this project is [Jason Yeomans](jyeoman2@gmu.edu), and a lead developer is [Daniel Bond](dbond2@gmu.edu).

Please visit the [SRCT Wiki](http://wiki.srct.gmu.edu/) for more information on this and other SRCT projects, along with other helpful links and tutorials.

## Setting everything up for development

These instructions are for Ubuntu and Debian, or related Linux distributions. (If you'd like to help write the instructions for Mac's OSX, please do!)

### Prerequisities

### Package Installation

First, install python, pip, and git on your system. Python is the programming language used for Django, the web framework used by Roomlist. 'Pip' is the python package manager. Git is the version control system used for SRCT projects.

Open a terminal and run the following commands.

`sudo apt-get update`

This retrieves links to the most up-to-date and secure versions of your packages. Next, with

`sudo apt-get install python python-dev python-pip git`

you install python and git.

We're using Postgres for our database, so run

`sudo apt-get install postgresql postgresql-contrib python-psycopg2`.

### Copying Down the Source Code

Now, we're going to copy down a copy of the roomlist codebase from git.gmu.edu, the SRCT code respository.

Configure your ssh keys by following the directions at git.gmu.edu/help/ssh/README.

Now, on your computer, navigate to the directory in which you want to download the project (perhaps one called development/ or something similar), and run

`git clone git@git.gmu.edu:srct/roomlist.git`

### The Virtual Environment

Virtual environments are used to keep separate project packages from the main computer, so you can use different versions of packacages across different projects and also ease deployment server setup.

It's often recommended to create a special directory to store all of your virtual environments together, but some prefer keeping their virtual environment in the top level of their project's director. If you choose the latter, make sure to keep the virtual environment folders out of version control.

(For example, `mkdir ~/venv`, `cd ~/venv`)

Run `sudo pip install virtualenv`

to install virtualenv system-wide, and then run

`virtualenv roomlist`

in your virtual environment directory to create your virtual environment. Activate it by typing

`source roomlist/vin/activate`

If you ever need to exit your virtual environment, simply run

`deactivate`

Now, the packages you need to install for roomlist are in in the top level of the project's directory structure. Run

`pip install -r requirements.txt`

to in install all of the packages needed for the project.

Next, run `python manage.py makemigrations`, `python manage.py migrate`, then `python manage.py runserver`.

### Creating the Database

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

Type ``\q`` and hit enter to exit the PostgreSQL shell.

Copy the secret.py.template and config.py.template to secret.py and config.py respectively. For each, follow the comment instruction provided in each file.

Run `python manage.py syncdb` to set up the empty database tables. When you're prompted, say 'y' to setting up the superuser, but use your mason username and full mason email address (@masonlive.gmu.edu) for the account. This is because we use Mason's Central Authentication for our user signin, and your admin account needs to manage your CAS account.

## Starting up the test server

With your virtual environment active, run

`python manage.py runserver` in the directory with `manage.py`

Head over to localhost:8000 and see the site!

## Deployment

### Docker

For server deployment, not for most local work

## To-do

The list of to-do items is kept track of on the gitlab roomlist issues page. https://git.gmu.edu/srct/roomlist/issues

Each issue includes details about the bugs and features, and links to documentation and tutorials to help with fixing that specific issue.

Contact the project manager or any of its developers if you'd like help picking an unassigned issue.

## About Mason SRCT

**S**tudent - **R**un **C**omputing and **T**echnology (*SRCT*, pronounced "circuit") is a student organization at George Mason University which enhances student computing at Mason. SRCT establishes and maintains systems which provide specific services for Mason's community.
