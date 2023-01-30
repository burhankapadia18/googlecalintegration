# googlecalintegration
Google Calendar Integration



steps for setting up the project on your local machine:
- install docker or you can use virtualenv
- if you have docker in your system, run the following command to build the image "docker-compose build". and if you are using virtualenv then setup the virtual env and then activate it and then run the following command to install the dependencies "pip install -r requirements.txt".
- if using docker, to start the server run the following command "docker-compose up" else run "python manage.py runserver"
- also don't forget to place the client_secret json file in the main directory with name "client_secret.json".
