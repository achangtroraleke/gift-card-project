##Capstone Project: Gift Cards for small businesses

##Overview & Goal:
The Gift Card Web app is a solution for any small business to keep track of deferred revenue liability without having to commit to a Point of Sale company. Companies, such as Toast, UberEats, Doordash, offer this service as a premium feature with their service, after you have committed to using their payment system. So not only do small businesses have to pay the monthly fees of the agreement, but they must pay extra for these features they’ve already had. With the help of the Gift Card web app, a business can issue paper vouchers or certificates to consumers just as they used to, but the cards are now on record for the employee to redeem for them. Saving businesses hundreds of dollars every month.

##Tech Stack: Python/Django
I chose Django for its built-in authentication and its html templates. Since the emphasis is on data storage the focus of this project would be on the backend. 


##Features:
The system is not as simple as a spreadsheet that keeps track of outstanding amounts. Within the application’s interface, the user can record the gift card they issued at the time of purchase, by registering the customer who purchased it and the amount that was credited into the card. On redemption, the user can search the card by id or customer name, in case there are many outstanding gift cards in the database. Cards can only be redeemed or refunded based on the amount on the card. At the time of redemption or refund, a record of that action is added into the database, where a user can see the card’s activities. These records are useful to see trends of usage or prevent fraudulent claims by customers or employees. 

##How to run:
-Create a virtual enviroment and pip install requirements.txt
-Activate virtual enviroment
-Set DEBUG to True in settings.py
-Run python manage.py makemigrations in the command line
-Run python manage.py migrate in the command line
-Finally python manage.py runserver

##Database Schema
![schema image ](/schema.jpg)

##Testing
-To test run python manage.py test

