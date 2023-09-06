# iris-size-django
A portal for visualizing and keeping track of memory usage of an InterSystems IRIS instance.

## Usage
1. Clone this repository
   ```
   git clone ...
   ```
1. Make sure you're in /iris-size-django directory on your terminal and type
   ```
   pip install -r requirements.txt
   ```

Before the following steps, check the default schema on the management portal:

System Administration > Configuration > SQL and Object Settings > SQL > Default Schema

If it's different from SQLUser, depending on your installation and configuration you might get a DatabaseError [SQLCODE <-30>: \<Table or view not found\>]

Changing it back to SQLUser will correct the behavior in most cases, but I'm working on a solution on the Django side. 

3. Edit the DATABASE configuration on /iris-size-django/globalsize/settings.py to point to the database you wish to analyze and the namespace where the data should be stored.
    ```
    DATABASES = {
    'default': {
        'ENGINE': 'django_iris',
        'NAME': 'TEST',
        'USER': '_system',
        'PASSWORD':'sys',
        'HOST': 'localhost',
        'PORT':1972,
        }
    }
    ```

3. Execute the following commands on your terminal
   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

4. Follow the link http://127.0.0.1:8000/ (the same URL will be shown on your terminal)
5. Press update
6. Have fun!

   ![image](https://github.com/heloisatambara/iris-size-django/assets/81993336/57cfba5f-dbbd-4590-8c87-a1a47b285547)

# Additional information
If you have the default configuration, you will have a table called SQLUser.globals_iglobal on the selected namespace, if you wish to perform any treatment with InterSystems' products.

Also, you can check out step-by-step how this was developed on  the [A portal to manage memory made with Django](https://community.intersystems.com/post/portal-manage-memory-made-django-part-1) series of articles.

Feel free to contact me for any doubts!

 ### Credits
 The sorting algorithm was built from  https://dcode.domenade.com/tutorials/how-to-easily-sort-html-tables-with-css-and-javascript .
