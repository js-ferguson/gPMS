# gCLS - Goanna Clinic Listing Service

gCLS is a clinic listing service for small, ideally single practitioner health clinics.

The application is intended to be used by a practitioner to register their clinic in a searchable format with good google maps integration to make it easier for prospective customers/patients to find their clinic. The project is designed to fit into a larger overall project named gPMS or Goanna Patient Management System. The scope of gPMS is overall too large for this assessment project, so some features have been left to be implemented in a future release.


The live application can be viewed by going to [gCLS](https://goannapms.herokuapp.com/)


## UX

The application will be used by two main groups. Clinic owners/practitioners that register their clinic, including important details like a practitioner biography and clinic description as well as contact details and a link to their website. The registration process makes google maps integration simple by automatically geocoding the address and providing an easy way for the user to manually correct any geocoding errors that result in a misplaced map marker. The second group of users are people using the application to find clinics that offer the treatment they need. This is provided both by showing nearby clinics on the map, and by providing a search function allowing them to search a clinic name, a practitioners name, a city or street etc.

- Scenario 1 - A clinic owner decides that they would like to list their clinic with gCLS. They navigate to the site and on the landing page they find a signup form. They enter their details and check the box identifying themselves as a practitioner. They are taken to a second form where they can fill out personal details, including a bio and a list of modalities they provide ie. Acupuncture, Tuina Massage. Following that form there is a clinic registration form, where they get to add the details of their clinic including a description of the clinic, website and contact details and address. Once the registration is complete they are forwarded to their user profile where they can edit the previously provided details.

- Scenario 2 - A user is looking for a clinic nearby that provides acupuncture. They navigate to gCLS and on the map on the landing page, they can see that there are clinics in their area. They decide to register as a user of the site. They follow a similar registration process as a practitioner, however on the first form they omit the practitioner checkbox. When they get the the next form to enter personal details, there are no options to enter a bio or modalities, since these are irrelevant for a regular user of the site. Having successfully completed their registration, they are forwarded to their profile page where they can edit their previously provided details. From the search bar located in the Nav area, they can enter a search term. In this case they enter "acupuncture" and are presented with a list of all clinics, whos practitioners have specified acupuncture as one of their modalities. They click on one of the search results and are taken to the clinics profile. Here they can see all the details for that clinic including it's location on a map. clicking on the map marker at this point opens a new tab with directions from their current location to the clinic. 

 
### Wireframes

The finished project is somewhat different in design to the initial wireframes. Initially the project was inteded to be a full patient managemant system, providing patients with the ability to see available times at a clinic, and provide practitioners with a calendar/schedular to manage appointments as well as providing the ability to manage a patient contact list and case history. These features are still planned to be implimented in a future release.

![noFolio - Landing page](https://imgur.com/Ka8peKL.png)

![noFolio - Post view](https://imgur.com/nqYgq8U.png)

![noFolio - Create post](https://imgur.com/Nc30kk1.png)


### Screenshots

![noFolio - Desktop Screenshot](https://imgur.com/ywANj0E.png)

![noFolio - Mobile Screenshot](https://imgur.com/xuPFsbe.jpg)

## Features


### Existing Features

- Feature 1 - The landing page has a neat, minimalist design with easy navigation. The map is displayed as a banner which is functional and provides both a unique asthetic as well as a bit of colour and life to the page. 

- Feature 2 - Users can click on markers on the map to be taken to the clinic profile for the selected clinic.

- Feature 3 - The clinics profile page provides details of the clinic and also allows users to leave a review of the clinic. These reviews can be both edited or deleted by the user that created them.

- Feature 4 - The search feature accessed via the navbar makes use of postgresql's full text search feature to provide search result matches from text in multiple tables.

- Feature 5 - When a practitioner registers a new clinic, geopy is used with the provided address to get the clinics coordinates via google maps geocoding api. These are then used to add a marker for the clinic on the map. 

- Feature 6 - In the case that geopy gets the wrong coordinates, resulting in a map marker in the wrong location or if the clinic moves to a new premises, the coordinates can be updated by dragging the marker on the map to the new location and saving the change.

- Feature 7 - Updating a clinics address in the practitioners profile geocodes the new address so the marker changes location to the new premises. 

- Feature 8 - All other personal and clinic details can be edited in the users/practitioners profile page. 

- Feature 9 - Clicking a map marker gives a different result depending on what page the user in on. On the landing page and search page, clicking a marker takes you to the clinics profile page, where the map displays only that clinic. Clicking a marker on the clinics profile page opens a new tab with directions from the current location to the clinic.

- Feature 10 - Users registering an account cannot wander away from the registration process. Doing so should return them to the registration page they tried to navigate away from.

- Feature 11 - After signup, a regular user is directed to the search page. They are asked to enter a location to provide a default view of clinic that are nearby.


### Features Left to Implement

There are many more features that I intend to implement. I would like to put these in place immediately, but I have a course to finish.

* A notification system to let practitioners know via email/messages when their clinic revcieves a new review.

* Practitioners should have a calendar/scheduler where they can make appointment times available to be booked. 

* Appointments are handles as blocks of time. Blocks can be configured as either 30, 45, or 60 mins and can be restricted to certain modalities. So if a practitioner provides both acupuncture and massage as treatment option, they can make massages available only in the morning, or limited to a certain number per day... massages can be tiring.

* Blank time blocks can be inserted into the calendar, which can have custom labels. These can be used to schedule time that is unavailable for bookings. This could be to schedule lunch times, meetings, or time that the practitioner might need to be out of the clinic.

* A clinics profile page would list days in the upcoming week that have available times. Clicking on the "book now" link would take the user to a booking page that displays available times that can be booked.

* When a user books a time, they consent to having their personal details made available to the practitioner they book with. 

* Practitioners can set notifications to alert them to new bookings, Either by email or in a notification area in their scheduler. 

* When a new booking is confirmed, the users details are added to the practitioners contact management. This will include an area for pratitioners notes including red flags that may affect the way a treatment is performed, for instance "patient is pregnant" or "patient has Hep C"

* Clicking on an appointment in the scheduler takes the practitoner to the appointments management screen. Here the appointment can be cancelled, rescheduled, marked as a no-show etc. This page also has a link to the patients contact page and case file page

* A users profile page will display a list of all their upcoming appointments for the different clinics they use. they can cancel appointments here as long as it is more than 24 hours before the appointment. 

* Booking an appointment adds that clinic to the users "favourite clinics" list so they can easily book new appointments.

* Practitioners will have access to a full digital patient case file system. This could probably be a premium feature. 


## Technologies used

This project is predominantly written Python, using the Django framework. There are also a number of django extensions and python packages used as well, which are detailed in the requirements.txt. Some of the more notable ones include; django-phonenumber-field which integrates with the django orm and keeps phone numbers in a consistant format. Geopy, which uses the google maps geocoding api to geocode clinic locations. Whitenoise which is used to cache static files. Underpinning the entire project is PostgreSQL, a relational database which both stores all the content on the site and provides full-text searching. 

JavaScript was used to implement all maps functions and is also used to manipulate the DOM on profile pages to switch between the regular view and updating the users/clinics details.

Bootstrap classes have been used to provide basic layout and responsive design and as with my previous projects I used SASS rather than vanilla CSS3.


## Testing

I have performed extensive testing to ensure the application operates as expected. I have also had quite a few people using the site and reporting bugs and inconsistencies. Testing was performed manually by using the sites features as different users. First as a visitor without and account, then as a registered user, and finally logged in as a practitioner.

The layout has been tested for responsive design across all the platforms and screen sizes I have immediate access to, including; 

- Mobile Chrome on Android, ChromeOS and iOS
- Mobile Safari on iOS
- Mobile Firefox on Android
- Mobile Samsung Internet on Android
- Desktop Chrome on Windows, Linux and ChromeOS
- Desktop Firefox on Windows and Linux

### Validation and linting - Do validation

WC3 HTML validation is not passing due to Materialize.css using a deprecated media type. However, there are no flags for any of my own HTML

CSS Validation returns 31 errors and 782 warnings, all of which are in materialize.css and bootstrap.min.css. There was a single error in my own css, a stray comma. I fixed it.

I am working in Emacs and PEP-8 linting occurs every time I save my work. I also ran it manually before submission with no errors.

## Deployment

The project is hosted on Heroku and the code is available here on Github. The PostgreSQL server is running on a Digital Ocean droplet. 

It is possible to download and deploy the project yourself, making some minor modifications to create your own gCLS site. The following section provides deployment details, if you are interested in doing that. These are also the steps you can take if you would like to set up a development environment to contribute to the project.

First lets clone the repository, create a new python virtual environment and install the projects dependencies. This is also a good time to generate the apps secret key

1. Change to the directory where you keep your projects

```
user@somecoolhostname:~$ cd ~/code/
```

2. Make a local copy of the repository by cloning it with git

```
user@somecoolhostname:~$ git clone https://github.com/js-ferguson/gPMS
```

3. Next we will create a new virtual environment and generate a new secret key for your app. This will be saved in your environment variables later, so for now paste it somewhere for safe keeping. Navigate to the projects root directory and create a new python virtual environment

```
user@somecoolhostname:~$ cd gPMS && Python3 -m venv venv
```

4. This will create a virtual environment for you to install the apps dependencies without having to install them system wide. Now lets activate the venv and install the apps requirements.

```
user@somecoolhostname:~$ source venv/bin/activate && pip install -r requirements.txt
```

5. Now we want to generate a new secret key, start the python shell and import the secrets module

```
user@somecoolhostname:~$ python3
```
```
>>> import secrets
```
Then we create a 16 byte hex string 

```
>>> secrets.token_hex(16)
```
This will return a random string, copy it and save it for later when we set our environment variables. This will be the apps secret key.

quit out of python
```
>>> quit()
```


### Configuring PostgreSQL

gPMS uses PostgreSQL. Heroku provides a PostgreSQL plugin and I will detail how to add this to your Heroku deployment in the Deploy to Heroku section. It is also perfectly reasonable to install PostgreSQL on another service such as Digital Ocean, but I will not cover installation and configuration of a PostgreSQL server here.

### Configuring Google Maps API

For geocoding to function you will need to enable some Google Maps APIs in the Google Cloud Platform. Go to console.cloud.google.com and enable both the Maps JavaScript API and the Geocoding API. Take note of your key, you will need it for deployment.

### Configure stripe

To enable practitioners to subscribe to the service, you need to create a stripe account and enter your API keys in the env.py file. If you are deploying to heroku, you will need to add these keys to your config vars, found under the application settings in the heroku dashboard. 


### Environment variables

Rather than expose sensitive data like the apps secret key and database login details in the applications source code, we keep them in environment variables. If you are hosting the project locally on your own machine, you can edit the provided env.py.example file and save it as env.py. If you are deploying to Heroku or another service, you will need to add them in the configuration panel of those services. I will cover local deployment and deployment to Heroku.

The DEV environment variable is used to determine if the app is running in a development or production environment. If you are running with DEV=1 then debugging will be set to true.

#### Local Deployment

As previouly mentioned you can turn on debugging in your production environment by adding DEV=1 to your environment variables. You can do this by adding the following line to your .bashrc or .bash_profile

```
export DEV=1 
```

Before running the app for the first time you need to migrate the database to create the required tables, fields and relationships

```
python manage.py makemigrations
```

```
python manage.py migrate
```

If you are deploying locally for production, you can either set the DEV environment variable to DEV=0 or just don't set the varieble at all.

Edit the provided env.py.example file, adding the environment variable settings such as secret key, maps api key, database details and save it as env.py

Now you can run the application in the development server by running

```
python manage.py runserver
```

Then navigate to http://localhost:8000


#### Deploy to Heroku

The application already has a procfile and a requirements.txt, so there is no need to create those. 

Assuming you have an account at Heroku and are logged in, click new and create new app.

1. Add an app name, whatever you like. Select a region and hit "Create app"

2. Select "Heroku Git" as the deployment method and follow the instuctions to install the Heroku CLI tool, if you don't already have it installed. When you push the app the first time, it may fail to start because of missing environment variables and database. We can fix that now.

3. Go to Resources and under add-ons, search for postgres. Select Heroku Postgres from the dropdown and add it.

4. Click on settings and then "Reveal Config Vars".

Add these config vars with the values you saved earlier.

SECRET_KEY "r4nd0mH3x0f4bUncHof41ph4Num5"

MAPS_KEY "google maps api key"

These following variables are only necessary if you have your database hosted on another server. If you use the Heroku Postgres add-on the config vars are added automatically.

DB_ADDRESS "IP address or hostname of your database"

DB_PASS "password"

DB_USER "database owners username"

DB_NAME "name of the database"

STRIPE_PUBLISHABLE "your stripe pub key"

STRIPE_SECRET "your stripe secret key"

Now that you have entered your environment variables, you can either restart the app by clicking the "More" button in the top right and selecting "Restart all dynos" or you can just push the project again.

```
user@somecoolhostname:~$ git push heroku master
```

##### SSL Certificates

For the Google Maps API to function correctly the application needs to be hosted on a secure server. This service is only available on hobby and higher tier dynos which are paid services on Heroku. If cost is an issue you do have the option to host the project on your own apache server and get a free ssl certificate from letsencrypt.org

1. First you need to updrade your dyno to the hobby tier. From the dashboard, go to Resources and click "Change Dyno Type". Select Hobby.

2. Click on the profile image in the top right of the page and click Account Settings. Then click "Billing" and add your billing details.

3. From the Heroku dashboard, go to settings and scroll down to find SSL Certificates. Click "Configure SSL" and then select "Automatic Certificate Management". This will enable SSL for your dyno.

### SASS 

This project uses [SASS](https://sass-lang.com/), a CSS preprocessor that gives you access to some nice features not available with regular CSS. While I would usually add my style.scss file to my .gitignore, I have included it here so it is accessible for other developers. You will need to install SASS if you intend to make any styling changes. 

If you run windows you can follow the instructions to install SASS [here](https://www.impressivewebs.com/sass-on-windows/). Alternatively, you can install Windows Subsystem for Linux (WSL) and follow the rest of the instructions for Linux. Instructions to install WSL can be found [here](https://itsfoss.com/install-bash-on-windows/)

If you are on Mac check out [compass.app](http://compass.kkbox.com/)

If you run Linux you can use your package manager to search and install SASS and it's dependencies.

on Debian or Ubuntu:

```
user@somecoolhostname:~$ sudo apt-get install ruby-sass
```
on Arch:

```
user@somecoolhostname:~$ sudo pacman -S ruby-sass
```

3. Navigate to the static directory and set SASS to watch the sass directory for changes. This way updates to style.scss will be written to style.css every time it is saved

```
user@somecoolhostname:~$ sass --watch sass/:css/

```


## Bugs

As far as I am aware, all functionality works as intended. That's not to say that there are no bugs, but there are no major ones that I am aware of.

## Acknowledgements - update  me

There are some articles and documentation as well as some snippets of code that I found that were especially helpful.

First and foremost, I would like to thank Miguel Grinberg whos excellent [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) was an invaluable reference during the course of this milestone project.


#### Flask flashes
- https://getbootstrap.com/docs/4.0/components/alerts/
- https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/

#### WTForms
- https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/

#### WTForms custom validators
- https://wtforms.readthedocs.io/en/stable/validators.html
- https://hackersandslackers.com/guide-to-building-forms-in-flask/

#### Python Modules and Packages
- https://realpython.com/python-modules-packages/

#### Flask_login
- https://boh717.github.io/post/flask-login-and-mongodb/
- https://flask-login.readthedocs.io/en/latest/

#### Files uploads
- https://stackoverflow.com/questions/53890136/how-to-upload-multiple-files-with-flask-wtf
- https://www.geeksforgeeks.org/zip-in-python/

#### Mongo aggregation
- https://docs.mongodb.com/manual/aggregation/

#### Pagination
- https://www.youtube.com/watch?v=Lnt6JqtzM7I
- https://www.codementor.io/arpitbhayani/fast-and-efficient-pagination-in-mongodb-9095flbqr

#### Cloudinary and Flask
- https://medium.com/@johndavidsimmons/cloudinary-api-in-flask-14018d84a314


## References

#### Aggeregation pipeline
- https://stackoverflow.com/questions/57941559/how-to-get-a-count-of-documents-that-contain-keys-from-another-collection
- Stackoverflow user Chidram

#### Pagination using facet
- https://stackoverflow.com/questions/48305624/how-to-use-mongodb-aggregation-for-pagination?rq=1
- Stackoverflow user Alex Blex

#### User class for flask-login
- https://stackoverflow.com/questions/54992412/flask-login-usermixin-class-with-a-mongodb
- Stackoverflow user Sazzad
