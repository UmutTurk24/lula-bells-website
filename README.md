# lula-bells-website

In order to run the application:

Run: `source .venv/bin/activate` for the python env. I made sure that it gets automatically activated, but things can break. 

Install the packages `pip install -r requirements.txt`

Run the mysql db -> check the mysql folder

To create the database -> check the database folder

Run tailwindcss -> `npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch`

To run the website -> python3 main.py
It can't do full address resolution, so visit `https://127.0.0.1:5000/`. 

TBH I forgot where I left this project. I would recommend doing the following and letting me know how it goes:
    - log in to volunteer page and:
        - check the auth flow:
            - Emphasis on the: @login_required tag in main.py
            - All users (guest and admin) have access to this, so use any cred
            - You can check which users exist in the database/setup.py
        - search a student, add/remove/edit something using the UI
            - check this for each button. this should take quite some time. 
            - I should be done with them, but I am not sure. It's been a while.
            - Edit the UI and make it pretty if you think it is needed.

Once you are done with this, contact me. I believe last thing I was working on was the admin page. We can then talk about that. 