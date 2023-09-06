# iris-size-django

pip install -r requirements.txt

before the next steps, check the default schema on the management portal:
System Administration > Configuration > SQL and Object Settings > SQL > Default Schema
If it's different from SQLUser, depending on your installation and configuration you might get a DatabaseError [SQLCODE <-30>: <Table or view not found>]
Changing it back to SQLUser will correct the behaviour on most cases, but I'm working on a solution on the Django side. 

python manage.py makemigrations
python manage.py migrate
python manage.py runserver