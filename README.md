### General Info
***
This is a README file for the LMS Project created by Parv Pratap Singh (Roll no. 21f1002039) which contains the general know-how to operate the project.
## Technologies
***
A list of technologies used within the project:
* Flask
* Vue3
* Redis
* celery
## Installation
***
Please run the following commands on the terminal.
```
python -m venv .venv
.venv/Scripts/Activate.ps1 or source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
Once the setup is done, use the following script in the terminal to activate the virtual environment-
```
.venv/Scripts/Activate.ps1 or source .venv/bin/activate
```
Then use the following script in the terminal to run the code-
```
python main.py
python upload_initial_data.py
```
Use the following script to deactivate the virtual environment-
```
deactivate
```
To run the redis, celery and mailhog services-
```
redis-server
celery -A main:celery_app worker --loglevel INFO
celery -A main:celery_app beat --loglevel INFO
~/go/bin/MailHog
```
In case of any problem in running the redis server, run the following commands-
```
sudo killall redis-server
sudo service redis-server stop
```
To install all the vue dependencies for the frontend-
```
npm install
```
To start the frontend-
```
npm run serve
```