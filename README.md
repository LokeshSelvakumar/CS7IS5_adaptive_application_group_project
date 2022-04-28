# CS7IS5_adaptive_application_group_project
## Adaptive Investment Management
### To run the project:

Backend: <br>
- Start a virtual environment ```python -m venv env``` <br>
- Install packages in requirements.txt ```python -m pip install -r requirements.txt``` <br>
- Change directory to the ```investment_recommender```<br>
- Run command ```python manage.py migrate```, then ```python manage.py runserver```
<br>
Frontend:

The frontend is run on VSCode using [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
- Open project in VSCode
- Go to ```basicUI``` folder
- Click ```Go Live``` on bottom of screen
- Open webpage at http://127.0.0.1:5500/CS7IS5_adaptive_application_group_project/basicUI/login.html

**Sample Login:**<br> user: "1950809226",  password: "2H1Fk"

Telebot - BullFinch
To run the telegram bot, telegram application and a username on the telegram is mandatory.
- search Bullfinch in the telegram and you can find the bot with Dicaprio picture.
- Type '/start' or click 'start' button to kick start the sign up process.

To run the Bot script locally (Visual Studio code recommended): <br>
- Navigate to 'Refrences' directory and install all the dependencies in the requirements.txt file using the command pip install -r 'requirements.txt'
- to run the bot script use the command 'python tg-bottest.py'
