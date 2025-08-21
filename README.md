### STPproject

## clarification
This is a group college project, all the initial work is from my teammates and me, the initials two commits in this repositoriy  are made by the group, all the rest by me.

## Description
The Order-taking System (STP in Spanish) is a visual help to order on a Restaurant, it implement a display menu and an order cart, also it have a administer settings for the menu.   

## Funcionality:
At root you can select what are you: Client or Administrator.

For Administrator you have to Login, the creation of a Admin have to be done at shell with Django.
From Administrator you can create a new dish or modify an existing dish.

For Client you don't have to login.
From Client you can see the menu, add dishes to the cart, clear the cart and send an order.


Once the order is delivered, you can see the total price and add a review for the dishes ordered.

## How to run the server at localhost:

From the repository root (STPproject), you have to move at the "STP" directory.

> cd STP

Once there, you have to write

> python manage.py runserver

Now you can see the root view of the project by the following localhost direction.

http://127.0.0.1:8000

