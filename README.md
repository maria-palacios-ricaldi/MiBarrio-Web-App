# MiBarrio-Web-App
A Web Application assisting in Residential Location Decision-Making

This README provides a step-by-step guide on how to set up and run the web app on your local machine.


Prerequisites
Python: Ensure that you have Python 3.10.6 installed on your machine. If you need to download or update Python, visit the official Python website.

(https://www.python.org/downloads/)


-- follow the following steps & use the commands provide, in your terminal

1. Clone the Repository:

`git clone https://github.com/maria-palacios-ricaldi/MiBarrio-Web-App.git`
`cd MiBarrio-Web-App`

2. Setting Up a Virtual Environment:
To create a virtual environment to manage the project dependencies separately

`python -m venv venv`
`source venv/bin/activate`  # On Windows, use `venv\Scripts\activate`

3. With the virtual environment activated, install the project dependencies.

`pip install -r requirements.txt`

4. Database Migrations:
Ensure that the database is up-to-date with the necessary migrations.

`python manage.py migrate`

5. Running the Web App:
Start the development server.

`python manage.py runserver`


You should now be able to access the web app by visiting http://127.0.0.1:8000/ in your web browser.
