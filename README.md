# ROOMLIST

Roomlist is a secure, privacy-oriented service for Mason students to find their on-campus neighbors.

## On Contributing

Roomlist welcomes all the help it can get. Even if you don't feel like you can be helpful the more technical aspects, we definitely need designers, technical writers, and testers.

There are many things that can be done with this project (see the "To Do" section), but sometimes it's the small things that count, so don't be afraid of contributing just a small spelling mistake.

If you need help at all please contact a SRCT member. We want people to contribute, so if you are struggling, or just want to learn we are more than willing to help.

The project manager for this project is [Jason Yeomans](jyeoman2@gmu.edu), and a lead developer is [Daniel Bond](dbond2@gmu.edu).

Please visit the [SRCT Wiki](http://wiki.srct.gmu.edu/) for more information on this and other SRCT projects, along with other helpful links and tutorials.

## Setting everything up for development

These instructions are for Ubuntu and Debian, or related Linux distributions. (If you'd like to help write the instructions for Mac OSX, please do!)

### Prerequisities and Package Installation

First, install python, pip, and git on your system. Python is the programming language used for Django, the web framework used by Roomlist. 'Pip' is the python package manager. Git is the version control system used for SRCT projects.

**Debian/Ubuntu**

Open a terminal and run the following commands.

`sudo apt-get update`

This retrieves links to the most up-to-date and secure versions of your packages. Next, with

`sudo apt-get install python python-dev python-pip git`

you install python and git.

Next, install these packages from the standard repositories

`$ sudo apt-get install libldap2-dev mysql-server mysql-client libmysqlclient-dev python-mysqldb libsasl2-dev libjpeg-dev redis-server`

If prompted to install additional required packages, install those as well.

When prompted to set your mysql password, it's advisable to set it as the same as your normal superuser password.

Now you're ready to set up the Roomlist repository on your machine.

**macOS (Formerly OS X)**

This tutorial uses the third party Homebrew package manager for macOS, which allows you to install
packages from your terminal just as easily as you could on a Linux based system. You could use another
package manager (or not use one at all), but Homebrew is highly reccomended.

To get homebrew, run the following command in a terminal:
``/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

**Note**: You do NOT need to use `sudo` when running any Homebrew commands, and it likely won't work if you do.

Now you want to Python, pip, git, and MySQL (macOS actually ships with some of these, but we want to have the latest versions). We'll also install Redis, though this package is only relevant when testing the production environment. To do so, run the following command in your terminal:

`brew install python git mysql redis`

Now you're ready to set up the Roomlist repository on your machine.

#### Git Setup

Now, we're going to clone down a copy of the Roomlist codebase from git.gmu.edu, the SRCT code respository.

Configure your ssh keys by following the directions at git.gmu.edu/help/ssh/README.

Now, on your computer, navigate to the directory in which you want to download the project (perhaps one called development/ or something similar), and run

`git clone git@git.gmu.edu:srct/roomlist.git`

### The Virtual Environment

Virtual environments are used to keep separate project packages from the main computer, so you can use different versions of packages across different projects and also ease deployment server setup.

It's often recommended to create a special directory to store all of your virtual environments together, but some prefer keeping their virtual environment in the top level of their project's director. If you choose the latter, make sure to keep the virtual environment folders out of version control.

(For example, `mkdir ~/venv`, `cd ~/venv`)

Run `sudo pip install virtualenv`

to install virtualenv system-wide, and then run

`virtualenv roomlist`

in your virtual environment directory to create your virtual environment. Activate it by typing

`source roomlist/bin/activate`

If you ever need to exit your virtual environment, simply run

`deactivate`

Now, the packages you need to install for Roomlist are in in the top level of the project's directory structure. Run

`pip install -r requirements.txt`

to in install all of the packages needed for the project.

### Creating the Database

Roomlist is configured for using a mysql database, (though you can change this in config.py)
By default, the database is called 'roomlist' in the configurations, and the user, 'roommate'.

Load up the mysql shell by running

``mysql -u root -p``

and putting in your mysql password.

Create the database by running

``CREATE DATABASE roomlist;``

You can choose a different name for your database. Double check your database was created

``SHOW DATABASES;``

Though you can use an existing user to access this database, here's how to create a new user and give them the necessary permissions to your newly created database.

``CREATE USER 'roommate'@'localhost' IDENTIFIED BY 'password';``
For local development, password strength is less important, but use a strong passphrase for deployment. You can choose a different username.

``GRANT ALL ON roomlist.* TO 'roommate'@'localhost';``
This allows your database user to create all the tables it needs on the roomlist database. (Each model in each app's models.py is a separate table, and each attribute a column, and each instance a row.)

``GRANT ALL ON test_roomlist.* TO 'roommate'@'localhost';`` ``FLUSH PRIVILEGES;``
When running test cases, django creates a test database so your 'real' database doesn't get screwed up. This database is called 'test_' + whatever your normal database is named. Note that for permissions it doesn't matter that this database hasn't yet been created.

The .\* is to grant access all tables in the database, and 'flush privileges' reloads privileges to ensure that your user is ready to go.

Exit the mysql shell by typing `exit`.

Now, to configure your newly created database with the project settings, and set up your project's cryptographic key, copy the secret.py.template in settings/ to secret.py. Follow the comment instructions provided in each file to set your secret key and database info.

Also copy config.py.template to config.py. You won't need to make any changes here off the bat. See more information about this file under the 'Deployment' section.

Run `python manage.py makemigrations` to create the tables and rows and columns for your database. This command generates sql code based on your database models. If you don't see output noting the creation of a number of models, add the app name to the end of the command, e.g. `python manage.py makemigrations housing`.

Then run `python manage.py migrate` to execute that sql code and set up your database. Migrations also track how you've changed your models over the life of your database, which allows you to make changes to your tables without screwing up existing information.

Finally, run `python manage.py createsuperuser` to create an admin account, using the same username and email as you'll access through CAS. This means your 'full' email address, for instance *gmason@masonlive.gmu.edu*. Your password will be handled through CAS, so you can just use 'password' here.

(If you accidentally skip this step, you can run `python manage.py shell` and edit your user from there. Selectyour user, and set .is_staff and .is_superuser to True, then save.)

## Loading in initial data

The project includes a json file to load majors into the database. Run `python manage.py loaddata accounts/major_fixtures.json`. You'll see output saying 'Installed 79 objects from 1 fixture(s) if all goes smoothly.

To add all freshman housing, with the virtual environment enabled, run `python manage.py shell < housing/housing_obj_creator.py`. It will take a couple of minutes, but this script will create every building, floor, and room in your database.

## Starting search

To start off indexing your models for searching, run `python manage.py update_index`.

## Starting up the test server

With your virtual environment active, run

`python manage.py runserver` in the directory with `manage.py`

Head over to localhost:8000 and see the site!

## Configuring the Social Media Applications

Social media authentication is provided through a package called [django-allauth](http://django-allauth.readthedocs.org/en/stable/installation.html). You can refer to those documentation pages for more information. Though in too many cases, the documenation is annoyingly sparse. The gulf between power of the package as shown through diving into the source and reading the documentation is vast.

What we're trying to accomplish with social media authentication is to verify users are linking to accounts they actually control. If we trusted users sufficiently to not type in gibberish or link to twitter.com/realDonaldTrump, we could provide a character field for each site.

Head over to localhost:8000/admin. Under 'Social Accounts', click on 'Social Applications'. Click 'Add social application' in the upper right hand corner. We're going to start off by adding Facebook.

### Facebook

To fill in the name, id, key, and site for Facebook, (and for all of the social media sites), you'll need to become a Developer for the site in question.

Navigate to, for example, the Facebook web login [documentation page](https://developers.facebook.com/docs/facebook-login/web). On the toolbar across the top of the page, you'll see a tab called 'My Apps'. Hovering over it, you'll see the option to Register as a Developer. Click the link, accept the Facebook platform and privacy policies, and you'll be ready to go. Depending on how fleshed out your profile page is, you may be prompted for more information (such as a phone number).

On the page you'll be [redirected to](https://developers.facebook.com/quickstarts/), select the website option. You'll be prompted to type the name of your new app. Because Facebook does not require apps to have globally unique names, go with something simple, like 'roomlist'. A dropdown will show an option to create a new app. Put Education as the category. Click on 'Create App ID'. If you see an option for 'namespace', skip over that for now: that's used for specifically defining the app's name via Facebook's API. For the line labeled 'Site URL', type 'localhost:8000'. Hit 'next' and then click the link on the section that lists functionality that says 'Skip to Developer Dashboard'. (For the record, we're implementing the Login functionality.)

You may be prompted to complete a captcha, and you'll then be shown your app's dashboard. The two things you need on roomlist are right up at the top, the App ID and the App Secret.

The user interface might be a bit different, particularly if you've done development with Facebook before, and some of these fields you may need to add after you've created the app. You may need to click 'Add Platform' from the Settings page of your app's Dashboard instead.

Back on the Django admin page, start filling in fields. App Name to Name, App ID to Client id, App Secret to Secret Key. The 'Sites' section is a security measure to ensure your app is only called from the urls you expect, and is what you put in for the 'Site URL' for the Facebook configuration.

Under 'Available Sites', click the little green plus button and add a new site. The Domain Name will be '127.0.0.1' and the Display Name 'localhost'. By default, Django has already gone to the trouble of creating 'example.com' as a site. Move example.com back to available sites and make sure 127.0.0.1 is added to Chosen Sites.

By default, example.com is the first site. We'll add our site id, localhost. In settings.py, this is already accounted for; the default there is SITE_ID = 2.

Let's add localhost to our Available sites, and then hit save.

Something you'll need to carefully specify is the callback (or redirect) url. This is where your user is sent once they have successfully authenticated with the outside social media site.

### Instagram

Instagram actually asks you what you want to build and then will choose to give you access or not. Cross your fingers and let's begin the process.

Sign up as developer on Instagram's [developer site](https://www.instagram.com/developer). Click on 'register your application'. You'll be asked a couple things. For your website, use localhost:8000. If your Instagram account does not have a phone number, you'll be asked to provide it here. Finally, for what you want to build with the API, write something along the lines of 'Verify users are linking to social media accounts they in fact control.' Accept the terms and sign up.

Interestingly, you'll be redirected to the 'Register Your Application' page. Click on 'Register Your Application' once more. From the next page, 'Manage clients', click 'Register a New Client ID'. On this form, for your Application name, you can also be generic; this does not need to be globally unique. For the description, you can use the same signup description you used initially. All fields except privacy policy are required, so use 'SRCT' as the company name. The website url will be http://localhost:8000. The 'http://' is required. For the valid redirect URI, Instagram takes a different tact than the other oauth2 applications. You will need the full redirect path. Type http://localhost:8000/accounts/instagram/login/callback/. The trailing slash is for some reason important. Because you can support multiple URIs, then hit tab. Use a real contact email. The privacy policy is not required. Complete the captcha and hit 'Register'.

Now add this information back into the Django admin. Create a new social application, and copy the client name to name, the client id to client id, and client secret to secret key. Make sure localhost is chosen as your site, and hit save.

### Twitter

Create a new social application, selecting Twitter as the provider.

Head to the Twitter [developer's page](https://dev.twitter.com/). Sign in, and go to apps.twitter.com and click 'create a new app'. Twitter does not require you to register as a developer up front, there is merely an agreement at the bottom on the new app page. You will, however, be required to add and verify your phone number to your Twitter account profile before submitting any apps.

Unlike the previous two sites, your app name must actually be globally unique. Pick, for example, 'roomlist-1234'. Next, your description will actually be shown to users when they sign in, so make sure it's reasonably coherent. Write something like 'verify your twitter account for roomlist'. For the website, use http://127.0.0.1:8000/. Use the same address for the callback, http://127.0.0.1:8000/. Agree to the developer terms, and click 'create your application'.

Next, by default, Twitter gives you more permissions than you actually need. On the app's page. click to the 'Permissions' tab. As we do not need to write to the users' Twitter account pages, select 'Read Only', and update your settings.

Now, click to the tab 'Keys and Access Tokens', and copy the 'Consumer Key' to Client ID on your new social application, and the 'Consumer Secret' to Secret Key. Make sure the name is the unique one you gave your app. Set localhost as your Site, and click Save.

### Google

Google's auth setup process is unquestionably the most confusing of the bunch, and yet we proceed, despite the ceiling of students who will link their Google+ page being approximately four.

Verify you have your phone number associated with your Google account, and then head to Google's [developer page](https://developers.google.com/). On that page, click 'Web'. Under the column titled 'Develop', click 'Sign In', and then click 'Get Started'.

The first step, will link you to the Google Developer's console. Click that link, then, intuitively (/s) click 'Select a Project' in the navbar, and then 'Create a Project' in the dropdown.

Type 'roomlist' in the project name field. Google will give you a globally unique project name underneath the field. Agree to the terms, and click 'create'.

Project name-- google gives you the project name

Go now to 'enable and manage APIs'. On the new screen under 'social APIs', click Google+ API. Click 'enable API', and then on the sidebar click 'credentials'. Then click 'add credentials', and 'oauth2 client id' under the dropdown. You will be asked to first configure a user consent screen (similar to the description we wrote for the Twitter client's authentication page). The only required field is your project name. Save, and then on the screen 'create client ID', click 'web application'. Name your project roomlist (this is only for your piece of mind, the actual name you'll use for Django is still the one Google generated for you), the authorized javascript origin is http://127.0.0.1:8000, without the trailing slash. For the authorized redirect url, type the full path like with Instagram, but inexplicably use 'localhost': http://localhost:8000/accounts/google/login/callback/, and *with* the trailing slash. Click 'Create'.

Copy the Client ID and Client Secret from the popup window that you'll then see into the Django social app's Client ID and Secret Key, respectively. Unless you delete the preceeding and trailing space when you copy the hashes, you will be sad because your string will be wrong.

If you've forgotten the name with the number, back on Google's page it's in the navbar, if you click on the more human-readable app's name.

Add localhost as the site, click save, and throw a party, because thank goodness, you're finally all set.


### Github

Github's auth setup is mercifully comparatively easy. Sign in and go to https://github.com/settings/applications/new. (Note if you're creating a token for an organization, you'll need to instead go to 
https://github.com/organizations/srct/settings/applications/new/. App names do not need to be universally unique. Set http://localhost:8000 as your Homepage URL. Your description will be shown to your users; write something like 'Verify your Github account with Roomlist!'. For the authorization callback, use http://localhost:8000/accounts/github/login/callback/. Note your Client ID and Client Secret in the refreshed page, and add a new social application. Copy everything over directly from your just configured Github OAuth Application page, and add localhost as your chosen site.

### Tumblr

Head to https://www.tumblr.com/settings/apps. The page is predominantly about Tumblr's mobile apps, but there's a faint gray line of text at the bottom. 'Wanna make an app? Cool. Register to use the Tumblr API, then have at it.' You'll need to verify your email address with Tumblr before continuing.

Click the '+ Register application' button, and then you'll have another page ahead of you to fill of OAuth information.
A couple of notes: the Application Name is not universal. Use the application description you've been using throughout, 'Verify your Tumblr account with Roomlist!'. The administrative contact email will be your Tumblr default account email. Set the callback url as http://localhost:8000/accounts/tumblr/login/callback/. Your application page icons cannot have transparent background. All right, you're ready to register!

On the Applications page that you'll be redirected to, the 'OAuth Consumer Key' is the Client ID you'll need when you add a new Social Application. Click 'Show Secret Key' to get the Client Secret. Use the name you gave your app, add localhost for your site, and you're off to the races.

Tumblr doesn't seem to have a way to only request specific permissions-- it will ask if it's okay both to access information and to post on your behalf. We're not interested in the latter, but keep in mind it will ask users if that's okay.

### Notes on Cacheing

Roomlist's urls are set to be cached for periods of time set so that ordinary user experience will not be impacted, but a substantial load will be lifted from a deployment server. However, this can be annoying when you're making and want to check small changes rapidly on development. You can edit the respective apps' urls.py files and remove the cacheing configurations, but make sure that you do not include such edits in any pushes!

## Deployment

A number of deployment-related settings have been moved from settings.py to config.py in settings/ for ease of use. Make sure to never have DEBUG mode on when running your project in deployment.

### Docker

For server deployment, not for most local work

## To-do

The list of to-do items is kept track of on the gitlab Roomlist issues page. https://git.gmu.edu/srct/roomlist/issues

Each issue includes details about the bugs and features, and links to documentation and tutorials to help with fixing that specific issue.

Contact the project manager or any of its developers if you'd like help picking an unassigned issue.

## About Mason SRCT

**S**tudent - **R**un **C**omputing and **T**echnology (*SRCT*, pronounced "circuit") is a student organization at George Mason University which enhances student computing at Mason. SRCT establishes and maintains systems which provide specific services for Mason's community.
