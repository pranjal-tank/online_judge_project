# THEOJ

A plateform for code submission and evaluation inside docker containers. Incubated features like search problem by code, sort problem by difficulty level, user authentication, user verification.

supports c11, c++14, c++17, c++20, python3.

## Let's Begin

1. Install [Docker](https://docs.docker.com/engine/install/) and [Python3](https://www.python.org/downloads/) on your system.
2. Install virtual environment. If pip is not install then install it first then run above command
```
pip install virtualenv
```
3. create virtual environment.
```
virtualenv virtualenv_name
```
4. Clone the repo
```
git clone <repo_link>
```
5. Install project dependencies from requirements.txt
```
pip isntall -r requirements.txt
```
6. Make migrations
```
python3 manage.py makemigrations
python3 manage.py migrate
```
7. Run local server
```
python3 manage.py runserver
```

# Screenshorts

<img src="https://user-images.githubusercontent.com/78424052/180066929-69826064-1ceb-49cd-aefd-3e531a007d44.png" width="500">
<img src="https://user-images.githubusercontent.com/78424052/180066911-786f5e46-f53b-4df4-876b-98580bc28095.png" width="500">  
<img src="https://user-images.githubusercontent.com/78424052/180066916-ca4478a6-c91d-4676-b3c2-ba9a21f62af6.png" width="500">
<img src="https://user-images.githubusercontent.com/78424052/180066920-5e58de73-38e7-4ead-b6c4-206ff91895d8.png" width="500">  
<img src="https://user-images.githubusercontent.com/78424052/180066925-f3df1311-d733-4b1a-b47d-b1fc65a26730.png" width="500">
