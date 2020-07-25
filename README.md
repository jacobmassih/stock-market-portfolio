# stockMarket
A portfolio to keep track of your investments in the Stock Market built as a web app using Django.

## Features
This app allows users to add U.S based companies in their portfolio and input the number 
of shares bought and the average cost for each company. Using the [IEX Cloud API](https://iexcloud.io/docs/api/),
data such as the stock close price is pulled and displayed to the user.
With this information, the app is able to determine the profit/loss for 
each stock and the overall performance of the stock portfolio over time, including its current market value.

## Technologies
This web app is created with :
- Django
- Python
- Bootstrap 4
- HTML & CSS

## Installation
To get this project up and running you will need to install the following:
  - [Python 3.8.3](https://www.python.org/downloads/release/python-383/)
  - Django
    - `pip install django==3.0.7`
  - Requests
    - `pip install requests`
    
    
## Setup
To run the web app, cd in the `src` directory of the project and run the following command:
```
python manage.py runserver
```
To access the web app go to `localhost:8000` in your web browser of choice.
