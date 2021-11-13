# BACKEND for MINI WALLET
The backend will have following functionalities

- Initialize my account for wallet
- Enable Wallet
- View My Wallet balance
- Add virtual money to my wallet
- Use virtual money from my wallet
- Disable wallet

## Running on local machine
The application is built with Django framework version 3.1.2
* Make sure Python and Django is installed
* Pull this repository, choose branch master
* Go to project directory /api 
```cd api
```
* Make migration with following commands
```python manage.py makemigrations
```
* then migrate
```python manage.py migrate
```
* Run the application
```python manage.py runserver
```
* If all goes well, the application will run on localhost. Ignore warning
```
Starting development server at http://127.0.0.1:8000/
```


## Testing the application
* Before using the application, create a customer account from the interface. Copy this url `http://127.0.0.1:8000/api/v1/` to a browser 
