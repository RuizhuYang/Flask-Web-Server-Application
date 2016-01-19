## Run the server-side application

Change directory project3, this will take you to the folder where the python files are. 

Run the python file databaseSetup.py to initialize the database. After this, I can find a database named cuisinewithusers.db in the project3 directory.

Run the python file addDishes.py to populate the database with some prepared cuisines and dishes (Optional).

Now, run the python file project.py to run the Flask web server. In your browser visit **http://localhost:8000** to view the cuisine category app. You should be able to login and logout, view, add, edit and delete cuisines and dishes.

To stop the web server, stop running the project.py python file.


## Funcionalities of this application

This cuisine category app provides a list of different dishes within a variety of categories and integrate third party user registration and authentication. Authenticated users should have the ability to post, edit, and delete their own cuisines and dishes.

To view the homepage of the application, visit **http://localhost:8000** in your browser. You can view all created cuisines on this page. To click the name of one specific cuisine, you can view all dishes of this cuisine. But you can not make any change to these information before your log in.

In order to login, please sign up a google account first. Once you have a google account, clikc the right-top *Please Login Here* button on webpage to login with your Google account. 

After logged in, you can create your own cuisine by clicking the *Add Cuisine* button on the webpage. The new cuisine you created will be shown on the homepage. For your own cuisine, you can edit, and delete it. And you can also add dishes into the cuisine category.

To add dishes, get into the webpage of one of your own cuisine, and click *Add Dish* button. After you add one dish, you can view it on the webpage of the specific cuisine. For your own dishes, you can edit, and delete it. 

After you logged in, you can click the right-top *Logout* button on webpage to log out anytime.


