## Project Overview
Developed an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Directory Structure
- Python module **project.py** runs the Flask application.
- A SQL database is created using the **database_setup.py** module and it was populated the with test data using **lotsofbookswithuser.py**.
- The Flask application uses the stored HTML templates in the templates folder &  & CSS file in the static folder to build the front-end of   the application.

## Instructions to run the project

### You will need
- [Python](https://docs.python.org/3/)
- [Vagrant](https://www.vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)


### Setup a Google Plus auth application
1. Go to https://console.developers.google.com/project and login with Google.
2. Create a new project
3. Name the project
4. Select "API's and Auth-> Credentials-> Create a new OAuth client ID" from the project menu
5. Select Web Application
6. On the consent screen, type in a product name and save.
7. In Authorized javascript origins add ``http://localhost:8000``
8. Click create client ID
9. Click download JSON and save it into the root directory of this project.
10. Rename the JSON file "client_secret.json"
11. In login.html replace the 'data-clientid' value so that it uses your Client ID from the web applciation.

### Setup a Facebook auth application
- [Create an APP ID](https://auth0.com/docs/connections/social/facebook)
- Go to your app on the [Facebook Developers Page](https://developers.facebook.com/).
- Click **+ Add Product** in the left column.
- Find **Facebook Login** in the Recommended Products list and click **Set Up**.
- Click **Facebook Login** that now appears in the left column.
- Add ``http://localhost:8000/`` to the **Valid OAuth redirect URIs** section.
- Create a file called fb_client_secrets.json file in the root directory of the repository.
- Paste the following into the fb_client_secrets.json file:
```
{ "web": { "app_id": "ENTER_APP_ID_HERE", "app_secret": "ENTER_APP_SECRET_HERE" } }
```

### Setup
* Install [Python](https://docs.python.org/3/), [Vagrant](https://www.vagrantup.com/), and [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
* Clone this repository.

### To Run 
1. From your terminal, go to the root directory of this repository.
2. Run the command ``vagrant up``. 
3. Once you got the shell prompt back, run the command ``vagrant ssh`` to log in to the Linux VM.
4. Run the command ``python database_setup.py``.
5. Use the command ``python lotsofbookswithuser.py`` to load the data.
6. To execute the program, run the command ``python project.py``.
7. Access and test the application by visiting ``http://localhost:8000``.
