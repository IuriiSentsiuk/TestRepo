# Project Name
#### Video Demo:  <URL HERE>
#### Description:

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->

## General Information
General information about the project:
- It's a simple budget planning management tool.

What problem does it (intend to) solve?
- System takes as basic data about your Savings (Owned cash, Pension savings, "Rainy days" ), incomes and costs (Salary, Monthly cash expenses), and the date you want to be retired. Based on this - you can get a result: the sum of Months needed to achieve your Goal (Desire), and the recommended sum that should be reserved as Saving for Retirement.

The purpose of the project:
- Keep your income and expenses under control

Why did I undertake it?
- For personal use as a self-written functionality for planning income and expenses.

## Technologies Used

- Python - version 3.10.5
- pip - version 22.2.2
- Flask - version 2.1.3
- bootstrap - version 5.1.3


## Features

List the ready features here:

- registration, authorization, and logout
- password hashing, user session verification
- Add cash. Calls a recalculation of the month's quantity wich will take to raise funds for each of your wishes
- Add/edit income and expense information
- Add information about the desired date of retirement, funds set aside for retirement, and the needed sum of Savings for that.
- The amount of minimum monthly deposits are calculated in order to collect the required amount of money before retirement on the date specified by the user
- Add desires and check the desires list.
- Buy desire - calls for a recalculation of the available cache, a recalculation of the months it takes to buy a desire.
- All calculations take into account the amount for a rainy day
- Viewing the history of replenishment of the cash balance and decreasing of balance if the desire is purchased. 

## Screenshots
![Balance](https://share.getcloudapp.com/xQuw1bWg)
![Desires](https://share.getcloudapp.com/4gurg2yl)

## Setup
Project requirements/dependencies:

> Python install [_Installation_](https://www.python.org/downloads/)

> Flask install [_Installation_](https://flask.palletsprojects.com/en/2.1.x/installation/)

Use Python and a library called Flask.
It is also a framework, where the library of code also comes with a set of conventions for how it should be used. For example, like other libraries, Flask includes functions we can use to parse requests individually, but as a framework, also requires our program’s code to be organized in a certain way:
- app.py will have the Python code for our web server.
- requirements.py includes a list of required libraries for our application.
- static/ is a directory of static files, like images and CSS and JavaScript files.
- templates/ is a directory for HTML files that will form our pages.


Start local server server with running flask run


## Usage
Use @login_required before call all the function. @login_required is presented in helpers.py

```
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
```


Function to display errors
```
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code
```


## Room for Improvement


Room for improvement:
- Use classes
- Recall methods


To do:
- Create 3 classes for users,  transactions and desires
- Write CRUD methods
- Write methods to calculate data


## Acknowledgements

- This project was inspired by Iurii Sentsiuk
- This project was based on [CS50’s Introduction to Computer Science](https://cs50.harvard.edu/x/2022/).
- Many thanks to CS50 staff and SoftServe IT Academy


## Contact
Created by [IuriiSentsiuk](https://github.com/IuriiSentsiuk) - feel free to contact me!

