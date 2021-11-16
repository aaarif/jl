# BACKEND for MINI WALLET 

## Running on local machine
The application is built with Django framework version 3.1.2
* Make sure Python and Django is installed
* Pull this repository, choose branch master
* In the terminal or command prompt (cmd) , Go to project directory /api 
```cd api
```
* Make migration with following commands
```
python manage.py makemigrations
```
* then migrate
```
python manage.py migrate
```
* Run the application
```
python manage.py runserver
```
* If all goes well, the application will run on localhost. Ignore warning
```
Starting development server at http://127.0.0.1:8000/
```


## Testing the application
* Before using the application, We need to create a customer account from the interface. Copy this url `http://127.0.0.1:8000/api/v1/` to a browser. 
* Enter Customer name then click Submit button. We want to get customer id from the newly created customer
* To get the customer ID we need to login to Djago Admin interface. We need to create user admin. In the cmd prompt or terminal, use command `python manage.py createsuperuser` to create user admin. Choose user and password that's easy to remember eg. `admin` for user, `admin123` for password
* Open this url `http://127.0.0.1:8000/admin` in a browser, you will see admin interface of the app. Input username and password that you created before
* In the Site Administration, under MyApp appears object Customers that contain the information of a customer that you created, copy the uid somewhere. We want to start using it to test
```
Home › Myapp › Customers › Customer object (6ecb8243-79cb-46fb-9969-bf1729c2567c)
```
* We need postman to test. Each end point serves for each purpose. Refer to documentation for request payload

**Initialize my account for wallet**  , use the customer id as form-data in request body.
```
POST http://127.0.0.1:8000/api/v1/init
```

**Enable Wallet**
```
POST http://127.0.0.1:8000/api/v1/wallet
```

**View My Wallet balance**
```
GET http://127.0.0.1:8000/api/v1/wallet
```

**Add virtual money to my wallet**
```
POST http://127.0.0.1:8000/api/v1/wallet/deposits
```

**Use virtual money from my wallet**
```
POST http://127.0.0.1:8000/api/v1/wallet/withdrawals
```

**Disable wallet**
```
PATCH http://127.0.0.1:8000/api/v1/wallet
```
