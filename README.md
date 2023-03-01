# Budget Tracker
#### Video Demo: [yourube video] <https://youtu.be/oItxm2nAF44>
#### Description:
The Budget-Tracker is a website that allows you to keep track of your expenses and savings. For this project I used as a guideline the Week 9 finance assignment. I used the "backbone" of this website to build on top my own site.

With this website you are able to keep track of your balance, which is edited by the income and expenses you input to it and also keeps track of your savings.

It has the same folders as the finance assignment (flask session, static and templates). It also contains a main .py file with the main code and a helpers.py for additional code.

For the finance.db I kept the users table and modified it to include the balance and savings of each user. I aded a new table labled "new". In this table I stored the data that each user inputs in the tracker. This contains the savings, expenses, income, and details about each transaction as what type of transaction it is (income, expenses or savings).

For the static folder I redesigned the look of the webpage and changed some aspects. My website has a side navigation bar and a different style with green/black tones.

### Templates:
For the templates folder I've kept the apology.html but modified it a bit to fit the style of the page.
There is a layout.html to keep the same style throughout the different htmls.
The login.html contains the login interface with a link to the register page in case you haven't signed up.
The register.html has also a link to the login in case you are already a user.
The index.html it’s the first page you encounter when you login. Here you can see your current balance and your savings up to date.
The tracker.html is where you can input your transactions. I decided to limit the type of transactions on income, saving and expense to be able to manipulate the balance and savings more easily. It contains a new entry button that inputs the data inot the database.
The history page is where you can see all the transactions added. I added a delete button so you can specifically remove transactions that the user might have inputed incorrectly or by mistake.

### The .py files
The helpers.py contain the apology function as well as the login_required function. The apology comes up when the user inputs wrong data. The login_required makes it so that the user must be logged in to be able to use the website.

From the app.py which is where the main code is. The structure is similar to the week 9 finance problem. For the history function it is fairly simple and used to populate the history.html table. One of the biggest challenges here was to make the delete function. The first problem with this was that I couldn't make it delete the specific transaction and it ended up either deleting them all or the first one. Here I used the for loop inside the html and the request.form to pair the clicking of the button with my delete function. The second problem I encounter was that by deleting this transaction the balance or savings in the home page did not update. So, I did a couple of if statements to update the values depending on what type of transaction was being deleted.

The next function is the tracker. The challenge here was that if the user chose as type "income" then the amount inputted would go to the income column and the savings and expenses would remain at 0. Again, I used if/else statements to be able to get this. For the "type" slot in the html I wanted to make a drop-down menu, but I wasn't able to get the if/else statements to work so opted for it to be something the user has to write.

For the index function it was fairly simple just added a date stamp and similar code was used to disable the index table as the history table. This is the home page so you can see the date and your current balance and savings.

The login and logout function I used the code from the week 9 project.

For the register function I used the code I made to solve the week 9 project and added the balance and savings to be set to 0 for the new user.



