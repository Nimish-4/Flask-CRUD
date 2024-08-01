# Description

This is a FLASK CRUD app with REST API endpoints for a user resource with the fields - name, e-mail and password. The data is stored in MongoDB which gives an additional unique ID to each field.

# How to run

Foremost, create a .env file in your root directory and add your MongoDB Atlas connection string as an environment variable in the file, since 'app.py' imports it from the .env file. You may also use local URI but MongoDB Atlas is preferred. Sample - 

```python
MONGO_URI = "mongodb+srv://<username>:<password>@co-rider.2n4ihqd.mongodb.net/<your_database_name>?retryWrites=true&w=majority&appName=Co-rider"
```

All the required modules are given in 'requirements.txt'. Since this project is meant to use docker, Dockerfile and .yml files have been created. To run the project, enter the command in the root directory through bash or some other terminal.

```bash
docker-compose up --build 
```
The flask app runs on the local port 5000 (http://127.0.0.1:5000). Requests can be sent through '/users' routes. Example - 

`POST http://127.0.0.1:5000/users`
`JSON payload = {'name':'...','email':'...','password':'...'}`

# Functionalities

1 - Basic rate limiting.

2 - Schema validation

3 - Password validation and cross-check.
