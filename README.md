# Thefacebook

As shown in The Social Network movie built with Python using the Django Web Framework.

### Demo

Check the website at [http://thefacebook.pythonanywhere.com](http://thefacebook.pythonanywhere.com/)

**Welcome Page**

![Thefacebook Screenshot](https://image.ibb.co/dGtsHJ/thefacebook_screenshot.jpg "Thefacebook Screenshot")

**Profile Page**

![Thefacebook Profile Screenshot](https://image.ibb.co/jpnoPy/thefacebook_profile_screenshot.jpg "Thefacebook Profile Screenshot")

### Installation Guide

Clone this repository:

```shell
$ git clone https://github.com/thetruefuss/thefacebook.git
```

Install requirements:

```shell
$ pip install -r requirements.txt
```

Copy `.env.example` file content to new `.env` file and update the credentials if any.

Run Django migrations to create database tables:

```shell
$ python manage.py migrate
```

Run the development server:

```shell
$ python manage.py runserver
```

Verify the deployment by navigating to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your preferred browser.
