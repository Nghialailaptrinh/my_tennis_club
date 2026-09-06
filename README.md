# My Tennis Club

A Django web application for managing and displaying tennis club members.

## Live Demo

Test the deployed website here:

http://my-first-django-env.eba-kt34xpjc.ap-southeast-2.elasticbeanstalk.com/

## Technologies

- Python
- Django
- PostgreSQL
- Bootstrap 5
- AWS Elastic Beanstalk
- AWS RDS

## Features

- Display tennis club members
- Browse classes, their teacher and enrolled members
- Browse teachers and the classes they teach
- Library placeholder page
- View member details
- Bootstrap 5 responsive styling
- PostgreSQL database
- Deployed on AWS Elastic Beanstalk

## Classes and teachers

Run `python manage.py migrate` before opening the new pages. In `/admin/`,
create classes and select existing members using the two-column member selector.
A class can have multiple members, and members can join multiple classes.
The teacher field is optional.
Public pages are `/classes/`, `/teachers/`, and `/library/`.

Run tests without connecting to the remote database:

```sh
python manage.py test --settings=my_tennis_club.test_settings
```
