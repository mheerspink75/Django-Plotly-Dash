# Project 4: Python Django

*A full description of the project scope criteria can be found [here](https://sites.google.com/view/reference-page/project-4).*

---
**Name:  Matt Heerspink**  
**Contact: mheerspink75@gmail.com**  
**Organization: Texas A&M University Kingsville**  
**Program:  Full Stack Web Development Bootcamp**  
**Project:  Python Django Finance Application**

---

## Abstract:  

Mach Trade is a cryptocurrency trading application that allows individual users to perform hypothetical trading of Bitcoin for USD.  Mach Trade uses external API requests from [Alphavantage](https://www.alphavantage.co/documentation/) and [Cryptocompare](https://min-api.cryptocompare.com/documentation) APIs to pull real-time data for Bitcoin USD exchange rates, time series performance history data and news stories which may impact the price of Bitcoin. All user BUY/SELL transactions, for hypothetical BTC/USD, are logged to the Django database. Portfolio performance is tracked through a combination of database queries and API data. Individual users are credited with $50,000 USD when a new user account is created. Portfolio balances and transaction histories can be reset from the Account page. 

---

**Install instructions**

**1.**  Clone the repoistory
```
git clone https://github.com/mheerspink75/Django-Plotly-Dash.git
```
**2.** Create a virtual environment in the cloned project directory
```
virtualenv django_project
```
**3.**  Activate the virtual environment
```
source django_project/scripts/activate
```
**4.**  Install the dependencies from requirements.txt
```
pip install -r requirements.txt
```
**5.**  Collect the static files
```
py manage.py collectstatic
```
**6.**  Migrate the Database
```
py manage.py makemigrations app1
py manage.py migrate
```
**7.** Create a user account and log in
```
py manage.py createsuperuser
```
**8.** Run the dev server
```
py manage.py runserver
```
dev server address:  http://127.0.0.1:8000/

---

## Workflow Requirements

### User Stories:

**1.** Cryptocurrency exchange rates are unpredicitable. I like the idea of making money trading Bitcoin but I don't have any experience trading Bitcoin. And, I don't want to lose money in the process. I want an application that allows me to perform hypothetical trades so I don't risk losing money while I'm getting started with cryptocurrency trading.

-*Mark*

**2.** I trade Bitcoin sometimes but I don't spend a lot of money on trading Bitcoin. I always wondered if I could make a million dollars trading Bitcoin. If I had $50,000 dollars to spend I would try to make a million on Bitcoin. I want an application that allows me to test my trading stratagies with out the risk of having to borrow the money.

-*Sarah* 

**3.** I'm a student. I don't have money to waist on Bitcoin right now.  I just want to know how to set up a Django 3 project, make finance API queries with python, display the data on some nice charts, get the database working and deploy the Django app that I'm working on. I might buy some Bitcoin someday.
 
-*Joe*  

---

### Development Phase:

**1.** Created Github repository [Django-Plotly-Dash](https://github.com/mheerspink75/Django-Plotly-Dash)

**2.** Set up virtual environment locally, created a new Django project and app.

**3.** Added Templates and Static Files folder structures to the app.

**4.** Once the basic skeleton of the site was functional I deployed the site to Heroku via Heroku CLI. Heroku Django deployment documentation can be found [here](https://devcenter.heroku.com/categories/python-support)

**5.** I created another Github repository to document the deployment process [here](https://github.com/mheerspink75/herokudjangoapp-deployheroku)

**6.** Added miniaturized [Bootstrap](https://getbootstrap.com/docs/4.4/getting-started/download/) CSS and JS files, miniaturized [jQuery](https://jquery.com/download/), miniaturized [Plotly.js](https://plot.ly/javascript/getting-started/) charting library to the project static files folder.

**7.** pip installed python pandas, pandas-datareader, dash, django-plotly-dash and django-crispy-forms to the virtual envrionment.

**8.** Wrote a series of python API requests to retrieve CSV and JSON data.

**9.** Created charts with python plotly and plotly.js to display data from the external APIs and from the Django database.

**10.** Created a registration page, login/logout page and user authentication system with Django Admin, Django Forms, django-crispy-forms, Django Templates and Bootstrap.

**11.** Created an Account model that credits the user $50,000 USD when the new user logs in for the first time and updates the Bitcoin and USD balances for the authenticated user when trades are placed from the user's account.

**12.** Created a Transactions model that logs the transacitions history of the authenticated user when trades are placed.  

**13.** Added a Reset button to allow the authenticated user to reset their Account balances and Transactions histories to their defaults.

**14.** Created a trading interface that allows the authenticated user to place BUY/SELL trades in either BTC or USD quantites, displays the current Bitcoin exchange rate, 24 hour and low price, updates the Account balances and displays the transaction history when trades are placed.

**15.** Created an account interface that allows the authenticated user to track their portfolio performance by displaying account balances and chart data.

**16.** Created a Quote interface that allows the user to track daily crypto currency prices and displays a time series chart.

**17.** Created a News page that pulls recent news stories from an API request.

