# Todo API
Rest API Project for Todo Apps

## Installation
To install this project on your computer or server, you can follow this instructions

#### 1. Clone this project

```bash
$ git clone https://github.com/ArRosid/todo_api.git
$ cd todo_api
```
#### 2. Create virtual environment and install requirements
```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
#### 3. Install Docker
This project used PostgreSQL inside docker as database server. So you need to install docker on your computer or server. You also need to install docker-compose to run docker-compose file that I have created for you. To install docker & docker compose, you can follow the instructions from docker documentations here:
  * https://docs.docker.com/engine/install/ubuntu/
  * https://docs.docker.com/compose/install/

#### 4. Start PostgreSQL
We will use docker to run PostgreSQL. First, you need to edit the username, password, and database name inside docker-compose.yml file
```yaml
...
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=db
...
```

To start the PostgreSQL, you can use the following command
```bash
$ sudo docker-compose up -d --build
```
*sudo* command is optional, If you use ubuntu, you need to use sudo. But if you use MAC, sudo is not necessary.

To make sure that the PostgreSQL is running, you can use this command
```bash
$ sudo docker container ls
```

#### 5. Create .env file
Inside todo_api directory, you will find .env.example file, copy this file to .env 
```bash
$ cp todo_api/.env.example todo_api/.env
```
And then edit the .env file
```bash
DEBUG=True
SECRET_KEY=secret
ALLOWED_HOSTS=*,
DATABASE_URL=postgresql://user:password@localhost:5432/db
```
  * Set the Debug to False if you want to deploy this project in production.
  * Configure the secret key using random string and make sure that you keep it private with you, never share it! 
  * Put your domain or IP Address in ALLOWED_HOSTS. If you have multiple domain or IP, you can put all of them and separate it using comma (,). Or you can just put * to allow any domain or IP
  * Edit the username, password and database name in the Database URL according to configuration in docker-compose.yml
  
#### 6. Migrate the Database
Do migrate to create database table according to Django models.
```bash
$ python manage.py migrate
```
#### 6. Create Super User
You need to create super user to manage the project from django admin
```bash
$ python manage.py createsuperuser
```
#### 7. Collectstatic
Get the static file for our project
```bash
$ python manage.py collectstatic
```
#### 8. Run the project
Now we are ready. You can try to run the project
```bash
$ python manage.py runserver 0.0.0.0:8000
```
Open your browser and go to [http://your_ip:8000/admin](http://your_ip:8000/admin) and login using user & password that you have created.

If you just want to run this project in development environment, you are done here. You can jump to the **Testing Section** to test the project.

#### 9. Create systemd socket & service for gunicorn
If you want to deploy this project in production, you need to do this step
```bash
$ sudo nano /etc/systemd/system/todoapi.socket
[Unit]
Description=Todo API socket

[Socket]
ListenStream=/run/todoapi.sock

[Install]
WantedBy=sockets.target
```
```bash
$ sudo nano /etc/systemd/system/todoapi.service
[Unit]
Description=Todo API daemon
Requires=todoapi.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/project/todo_api
ExecStart=/project/todo_api/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/todoapi.sock \
          todo_api.wsgi:application

[Install]
WantedBy=multi-user.target
```
  * Change User to your Operating System username.
  * Change WorkingDirectory & ExecStart to path where you save the project name

Now we need to enable & start the socked & service file
```bash
$ sudo systemctl start todoapi.socket
$ sudo systemctl enable todoapi.socket
$ sudo systemctl start todoapi.service
$ sudo systemctl enable todoapi.service
```
If you doing change in socket or service file, you also need to reload daemond
```bash
$ sudo systemctl daemon-reload
```
#### 10. Configure Nginx
Create and edit nginx site configuration for our project
```bash
$ sudo nano /etc/nginx/sites-available/todoapi 
server {
    listen 80;
    server_name todoapi.example.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /project/todo_api;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/todoapi.sock;
    }
}
```
  * Edit server_name to your domain or IP 
  * Edit location root to path where you save the project name

Enable the site configuration
```bash
$ sudo ln -s /etc/nginx/sites-available/todoapi /etc/nginx/sites-enabled
```
Last, restart the nginx service
```bash
$ sudo systemctl restart nginx
```
#### 11. Create Subdomain
This is optional step, If you have public domain, you can create subdomain and point it to your Public IP Address of your server. 

## Testing
To test this project, you can use the Django Rest Framework UI by visiting this urls
  * [http://your_domain/api/v1/login](http://your_domain/api/v1/login)
  * [http://your_domain/api/v1/todos](http://your_domain/api/v1/todos)
  
Or you can also use curl

#### 1. Login 
```bash
$ curl -X POST -d username=user -d password=password http://todoapi.example.com/api/v1/login/ | json_pp
{
   "refresh" : "refresh_token",
   "access" : "access_token"
}

```
#### 2. Create new todos
```bash
$ curl -X POST -d title="New todos from curl" -H "Authorization: Bearer access_token" http://todoapi.arrosid.com/api/v1/todos/ | json_pp

{
   "updated_at" : "2020-05-10T05:02:29.294021Z",
   "title" : "New todos from curl",
   "completed" : false,
   "id" : 3,
   "created_at" : "2020-05-10T05:02:29.294002Z"
}

```
#### 3. Get all todos
```bash
$ curl -H "Authorization: Bearer access_token" http://todoapi.arrosid.com/api/v1/todos/ | json_pp

[
   {
      "created_at" : "2020-05-10T03:36:49.898325Z",
      "id" : 1,
      "title" : "First todos test updated",
      "completed" : false,
      "updated_at" : "2020-05-10T03:36:57.415187Z"
   },
   {
      "title" : "Second todos test",
      "completed" : true,
      "updated_at" : "2020-05-10T03:37:16.859910Z",
      "created_at" : "2020-05-10T03:37:08.317532Z",
      "id" : 2
   },
   {
      "created_at" : "2020-05-10T05:02:29.294002Z",
      "id" : 3,
      "updated_at" : "2020-05-10T05:02:29.294021Z",
      "title" : "New todos from curl",
      "completed" : false
   }
]
```
#### 4. Edit todo
```bash
$ curl -X PUT -d title="New todos from curl updated" -H "Authorization: Bearer access_token" http://todoapi.arrosid.com/api/v1/todos/3/ | json_pp

{
   "completed" : false,
   "created_at" : "2020-05-10T05:02:29.294002Z",
   "title" : "New todos from curl updated",
   "updated_at" : "2020-05-10T05:05:49.886150Z",
   "id" : 3
}

```
#### 5. Mark todo as done
```bash
$ curl -X PATCH -d completed=True -H "Authorization: Bearer access_token" http://todoapi.arrosid.com/api/v1/todos/3/ | json_pp

{
   "created_at" : "2020-05-10T05:02:29.294002Z",
   "completed" : true,
   "id" : 3,
   "updated_at" : "2020-05-10T05:06:48.963501Z",
   "title" : "New todos from curl updated"
}
```
#### 6. Delete todo
```bash
$ curl -X DELETE -H "Authorization: Bearer access_token" http://todoapi.arrosid.com/api/v1/todos/3/
```

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/)

