# iSystemKids Backend API

## Overview

This backend API powers the iSystemKids platform for students, teachers, and admins.

It includes:

* JWT authentication
* User roles
* Lessons and homework
* Student rewards system
* Shop and todo features
* Avatar uploads
* PostgreSQL database integration

The project is built with FastAPI and Tortoise ORM.

---

## Tech Stack

* Framework: FastAPI
* Database: PostgreSQL
* ORM: Tortoise ORM
* Authentication: JWT
* Password Hashing: Passlib Bcrypt
* Image Processing: Pillow
* Database Migration: Aerich

---

## Base URL

```txt
http://localhost:8000
```

---

## Authentication

Protected endpoints require a Bearer token.

```http
Authorization: Bearer your_token_here
```

### Login

```http
POST /token
```

Request body:

```json
{
  "username": "student1",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

---

## User Roles

The API supports three roles:

* admin
* teacher
* student

---

## User Endpoints

### Get Current User

```http
GET /users/me
```

Returns the currently authenticated user.

### Get All Admins

```http
GET /admins
```

### Get All Teachers

```http
GET /teachers
```

### Get All Students

```http
GET /students
```

### Create User

```http
POST /create_user
```

This endpoint creates a new user and uploads an avatar image.

Supported avatar formats:

* png
* jpg

Example form fields:

```txt
name
last_name
username
email
password
role
avatar
```

### Delete Current User

```http
DELETE /delete_user
```

Deletes the authenticated user account.

---

## Lesson Endpoints

### Get User Lessons

```http
GET /get_lessons
```

Returns only lessons assigned to the currently authenticated user.

---

## Rewards System

Students can earn:

* Tokens
* Diamonds

### Get Diamond Balance

```http
GET /diamonds
```

Response:

```json
{
  "data": 5,
  "data2": 100
}
```

`data2` is calculated as:

genui{"math_block_widget_always_prefetch_v2":{"content":"y = 20x"}}

where:

* x = diamond balance
* y = converted value

### Give Tokens

```http
POST /give_tokens
```

Query params:

```txt
user_id
tokens_number
```

Only teachers and admins can give tokens.

Maximum allowed per request: 5

### Take Tokens

```http
POST /take_tokens
```

Only teachers and admins can remove tokens.

### Give Diamonds

```http
POST /give_diamonds
```

Only teachers and admins can give diamonds.

Maximum allowed per request: 5

### Take Diamonds

```http
POST /take_diamonds
```

Only teachers and admins can remove diamonds.

---

## Static Files

User avatars are stored inside:

```txt
/static/users/
```

The static directory is mounted with:

```python
app.mount('/static', StaticFiles(directory='static'), name='static')
```

---

## Included Routers

The following routers are connected in the main application:

```python
shop
lesson
homework
todo
```

---

## Database Configuration

The project uses PostgreSQL.

```python
postgres://isystem:isystem@localhost/isystem
```

Tortoise ORM models:

```python
['aerich.models', 'models']
```

---

## Example Error Response

```json
{
  "detail": "Invalid username or password"
}
```

---

## HTTP Status Codes

* 200 OK
* 201 Created
* 204 No Content
* 401 Unauthorized
* 404 Not Found

---

## Future Improvements

* Refresh tokens
* Better permission decorators
* Email verification
* Pagination
* Swagger examples
* Better validation for uploaded files
* Lesson filtering by role
* Store JWT expiration date

---

## Run Project

```bash
uvicorn main:app --reload
```

---

## License

MIT License
