# Conecopia Gelato LLC Ecommerce Website
(Currently still in development)

This is the Conecopia Gelato e-commerce platform. This platform is meant to replace the legacy gelato pre-ordering platform built back when I was in highschool. 


## Enviroment Variable Settings
```bash
DJANGO_SECRET_KEY=""

# Database
DATABASE_URL=""

# Mailgun
MAILJET_API_KEY=""
MAILJET_SECRET_KEY=""

# Object Storage
DIGITAL_OCEAN_ACCESS_KEY=""
DIGITAL_OCEAN_SECRET_KEY=""
STORAGE_BUCKET_NAME=""
STORAGE_REGION="nyc3"
STORAGE_ENDPOINT_URI="digitaloceanspaces.com"

# Stripe Payment Processor
STRIPE_PUBLIC_KEY=""
STRIPE_SECRET_KEY=""

DEBUG=False
ALLOWED_HOSTS="conecopia.com,conecopia.trysous.co"
```

## Technical Stack

### Front End

#### Standard HTML/CSS (No Frameworks)
I chose to use no frontend framework for this project because I felt that Django's built in templating syntax in combination with JQuery and vanilla JavaScript would be sufficent to all of the dynamic needs of this application. I also didn't want to use Django as a REST server as I wanted to experience the MVC architechture style that Django is known for.

#### Preline w/ Tailwind CSS
I used Preline in combination with Tailwind CSS to make dealing with styling easier. Rather than maintaining a varity of stylesheets in Django's static directory, I only have to deal with one master stylesheet. Preline helps as it contains a lot of prebuilt components that are already ADA compliant and well thought out. I used preline's components as a boilerplate to build off of.

### Back End

#### Python Django
I chose Django becuse I knew this project was going to be specialized. I felt that if at any point I needed to move beyong the scope of what the monolithic architechure could provide, then I'd have to rewrite most of my code anyway.

#### SQLite
The current version of my software uses SQLite 3 as its database. I chose SQLite because its portable, clean, and doesn't require any special infrastructure to develop on.

## License
© COPYRIGHT 2025, JOEL DESANTE, ALL RIGHTS RESERVED.

This software is not to be used for commercial or personal purposes by anyone except for the copyright holders Joel DeSante and exclusive license holders Conecopia Gelato LLC.

The source code is made publicly available only for the express purpose of being used as a demonstration of Joel DeSante's past work.
