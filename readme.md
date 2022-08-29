## Setup and run

**Run the following commands to get up and running**

1. `python3 -m pip install virtualenv`
2. `python3 -m virtualenv venv`

    

3. If OS is *Linux* or *macOS*,

    `source venv/bin/activate`

    If OS is *Windows*,

    `.\venv\Scripts\activate`

4. `cd maillogin`
5. `python3 -m pip install -r req.txt`
6. `python3 manage.py collectstatic`
7. `python3 manage.py makemigrations`
8. `python3 manage.py migrate`
9. `python3 manage.py createsuperuser`
10. `python3 manage.py runserver`
