# iris-size-django

A portal for visualizing and keeping track of memory usage of an InterSystems IRIS instance. It shows a table with a database path, global, allocated size and size in use for each global, and aggregation sums at the end.

![program screenshot](https://github.com/heloisatambara/iris-size-django/assets/81993336/f5d925af-e434-40f4-9a10-2d044c9e11a7)

Django Framework was chosen to easily migrate and exchange data from the instance to a web template.

Some features will have better error handling in the future.

## Instalation

1. Clone this repository

    ```sh
    git clone https://github.com/heloisatambara/iris-size-django.git
    ```

2. Make sure you're in /iris-size-django directory on your terminal and type

    ```sh
    pip install -r requirements.txt
    ```

    Before the following steps, check the default schema on the management portal:

    System Administration > Configuration > SQL and Object Settings > SQL > Default Schema

    If it's different from SQLUser, depending on your installation and configuration you might get a DatabaseError [SQLCODE <-30>: \<Table or view not found\>]

    Changing it back to SQLUser will correct the behavior in most cases, but I'm working on a solution on the Django side.

3. Edit the DATABASE configuration on /iris-size-django/globalsize/settings.py to point to the database you wish to analyze and the namespace where the data should be stored.

    ```python
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

4. Execute the following commands on your terminal

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```

5. Follow the link <http://127.0.0.1:8000/> (the same URL will be shown on your terminal)
6. Press update
7. Have fun!

## Usage

With the link <http://127.0.0.1:8000/> open on your preferred browser, add as many filters as you want and press Filter to activate them, choose from CSV, XML, or JSON, and press Export to get a file containing all information on the current table on the directory where you cloned the repository, and press any of the headers to order.

If you want to track the memory usage of a particular table, you can check which globals it uses on its storage and add their names on the filters.

### Additional information

If you have the default configuration, you will have a table called SQLUser.globals_iglobal on the selected namespace, if you wish to perform any treatment with InterSystems' products. If you want to save the data on a different instance, change the connection on /iris-size-django/globals/api/methods.py to the instance you wish to analyze, and in step 3, point to the storage.

Also, you can check out step-by-step how this was developed on  the [A portal to manage memory made with Django](https://community.intersystems.com/post/portal-manage-memory-made-django-part-1) series of articles.

Feel free to contact me for any doubts!

## Credits

The sorting algorithm was built from <https://dcode.domenade.com/tutorials/how-to-easily-sort-html-tables-with-css-and-javascript>.

## TODO

1. add filters for tablename, check if exporting works for tablename
2. Add testing
3. Correct for different Default Schemas
4. Make the connection editable by the client size
5. Make the file path editable by the client size or display the path after exporting
